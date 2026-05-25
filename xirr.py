import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scipy.optimize import newton

# -----------------------------
# CONFIG
# -----------------------------
YEARS = 5

# For scheme codes, use https://api.mfapi.in/mf/<scheme code> to verify

# Some investment guy's Regular fund recommendations
# FUNDS = [
#     {"scheme_code": "145456", "monthly_sip": 5000},
#     {"scheme_code": "145139", "monthly_sip": 10000},
#     {"scheme_code": "142109", "monthly_sip": 10000},
#     {"scheme_code": "109059", "monthly_sip": 5000},
#     {"scheme_code": "119159", "monthly_sip": 10000},
# ]

# My simple plan
FUNDS = [
    {"scheme_code": "122639", "monthly_sip": 20000},
    {"scheme_code": "118989", "monthly_sip": 10000},
    {"scheme_code": "130503", "monthly_sip": 10000},
]

# -----------------------------
# XIRR FUNCTION
# -----------------------------
def xirr(cashflows):
    def xnpv(rate):
        t0 = cashflows[0][0]
        return sum(
            cf / ((1 + rate) ** ((t - t0).days / 365.0))
            for t, cf in cashflows
        )
    try:
        return newton(xnpv, 0.12)
    except RuntimeError:
        return float('nan')

# -----------------------------
# PROCESS EACH FUND
# -----------------------------
def process_fund(fund):
    url = f"https://api.mfapi.in/mf/{fund['scheme_code']}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    scheme_name = data["meta"]["scheme_name"]

    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = df["nav"].astype(float)
    df = df.sort_values("date").reset_index(drop=True)

    today = df["date"].max()
    start_date = today - relativedelta(years=YEARS)

    # Build monthly SIP dates (1st of each month)
    sip_dates = []
    d = datetime(start_date.year, start_date.month, 1)
    while d <= today:
        sip_dates.append(d)
        d += relativedelta(months=1)

    cashflows = []
    units = 0
    monthly_sip = fund["monthly_sip"]

    for sip_date in sip_dates:
        nav_row = df[df["date"] >= sip_date]
        if nav_row.empty:
            continue
        nav = nav_row.iloc[0]["nav"]
        units += monthly_sip / nav
        cashflows.append((nav_row.iloc[0]["date"], -monthly_sip))

    latest_nav = df.iloc[-1]["nav"]
    portfolio_value = units * latest_nav
    cashflows.append((today, portfolio_value))

    invested = monthly_sip * (len(cashflows) - 1)
    xirr_val = xirr(cashflows)
    gain = portfolio_value - invested

    return {
        "name": scheme_name,
        "monthly_sip": monthly_sip,
        "invested": invested,
        "portfolio_value": portfolio_value,
        "gain": gain,
        "xirr_pct": xirr_val * 100,
    }

# -----------------------------
# RUN & PRINT
# -----------------------------
print(f"\n{'='*80}")
print(f"  SIP XIRR ANALYSIS — {YEARS}-YEAR REGULAR GROWTH PLANS")
print(f"{'='*80}\n")

total_invested = 0
total_value = 0
xirr_sum = 0

for fund in FUNDS:
    try:
        r = process_fund(fund)
        total_invested += r["invested"]
        total_value += r["portfolio_value"]

        print(f"  {r['name']}")
        print(f"  SIP    : ₹{r['monthly_sip']:>8,.0f}/month")
        print(f"  Invested: ₹{r['invested']:>10,.0f}   |   Value: ₹{r['portfolio_value']:>10,.0f}   |   Gain: ₹{r['gain']:>10,.0f}")
        print(f"  XIRR   : {r['xirr_pct']:.2f}%")
        print(f"  {'-'*76}")

        xirr_sum += r['xirr_pct']
    except Exception as e:
        print(f"  ERROR fetching {fund['name']}: {e}")
        print(f"  {'-'*76}")


total_gain = total_value - total_invested
print(f"\n  PORTFOLIO TOTAL")
print(f"  Total Invested : ₹{total_invested:>12,.0f}")
print(f"  Total Value    : ₹{total_value:>12,.0f}")
print(f"  Total Gain     : ₹{total_gain:>12,.0f}")
print(f"  Return         : {((total_value / total_invested) - 1) * 100:.2f}% (absolute)\n")
print(f"{'='*80}\n")

print("Average XIRR", xirr_sum / len(FUNDS))
