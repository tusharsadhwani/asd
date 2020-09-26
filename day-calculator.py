'''Neat little code to find out the day for a date.
Uses the fact that January 01, 0001 was a Monday, therefore
0 January 0000 would be a Friday. So we count the number of odd days
from then on and count up from a friday.'''

def main():
    '''Runs the main logic for day calculation'''

    # InputDate takes the 3 values and outputs them into these 3 variables.
    day, month, year = input_date()
    odds = 5  # 5 odd days in the beginning, as 0-1-0000 would be a Friday
    print("Beginning odds =", odds)
    print()

    # check if leap year, and calculate odd days based on day, month and year
    is_leap, odds = calculate_year(year, odds)
    odds += calculate_month(is_leap, month)
    odds += calculate_date(day)

    # Finally, after getting odd days, getting modulus 7 will give us the day
    get_day(odds)


def input_date():
    '''Takes input of date from stdin and parses it into date, month and year'''
    while True:
        date = input("Enter date <DD/MM/YYYY>: ")
        date = date.split('/')

        if len(date) != 3:
            print("Incorrect format, try again.")
            continue

        try:
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])
            break
        except ValueError:
            print("Incorrect format, try again.")

    print()
    print(
        "Input date:",
        '/'.join((str(day), str(month), str(year)))
    )
    print()
    return day, month, year


def calculate_year(year, odds):
    '''Calculates extra odd days based on year entered'''

    # Leap year check
    if year % 400 == 0:
        is_leap = True

    elif year % 100 == 0:
        is_leap = False

    elif year % 4 == 0:
        is_leap = True

    else:
        is_leap = False

    # Calculating odd days:
    # Any bunch of 400 years contributes to zero odd days,
    # hence dividing by 400 and keeping the remainder.
    year %= 400
    print("Modulus 400, years left =", year)

    # Every bunch of 100 years contributes to 5 odd days, provided years < 400.
    odds += 5 * (year//100)
    print()
    print("Each bunch of 100 years contributes 5 odd days")
    print("Adding", (year//100), "bunch of 100 years =", odds, "odd days now.")

    year %= 100
    print("No. of years left =", year)

    # Every bunch of 4 years gives 5 odd days, provided years < 100.
    odds += 5 * (year//4)
    print()
    print("Each bunch of 4 years contributes 5 odd days")
    print("Adding", (year//4), "bunch of 4 years =", odds, "odd days now.")

    year %= 4
    print("No. of years left =", year)

    if year > 0:  # The first year is already being counted as a leap year.
        odds += 2
        year -= 1
        print("Adding 2 odd days for leap year, no. of odds =", odds)
        print("Years left =", year)

        print("Finally adding", year, "odd days")
        # Every one year has one odd day provided those years are not leap years.
        odds += year

    print("Total odds =", odds)
    odds %= 7
    print("Hence, net odd days =", odds)
    print("Leap year =", is_leap)
    print()

    return is_leap, odds


def calculate_month(is_leap, month):
    '''Calculates extra odd days based on month entered'''

    odds = 0

    # Now adding no. of odd days according to months passed.
    # January has 3 odd days so add 3, if month is April add 6, etc.
    if month == 2:
        odds += 3
    elif month == 3:
        odds += 3
    elif month == 4:
        odds += 6
    elif month == 5:
        odds += 1
    elif month == 6:
        odds += 4
    elif month == 7:
        odds += 6
    elif month == 8:
        odds += 2
    elif month == 9:
        odds += 5
    elif month == 10:
        odds += 0
    elif month == 11:
        odds += 3
    elif month == 12:
        odds += 5

    print("Added", odds, "odd days according to month.")

    # Add one odd day if it is a leap year and February has already passed.
    if is_leap and month > 2:
        odds += 1
        print("Added 1 leap day to odd days.")

    print()

    return odds


def calculate_date(day):
    '''Calculates extra odd days based on date entered'''

    odds = day % 7
    print("Adding", day % 7, "odd days for", day, "days.")
    return odds


def get_day(odds):
    '''Finds the day based on odd day count'''

    print("Total odd days =", odds)
    odds %= 7
    print("Finally, net odd days =", odds)

    # Getting day out of odd days, 0  = Sunday, and onwards.
    print()
    print("So, the day is ", end='')

    day = {
        0: "Sunday!",
        1: "Monday!",
        2: "Tuesday!",
        3: "Wednesday!",
        4: "Thursday!",
        5: "Friday!",
        6: "Saturday!",
    }

    print(day[odds])

if __name__ == "__main__":
    main()
