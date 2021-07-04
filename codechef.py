import time
from datetime import datetime, timedelta
from typing import NamedTuple

from bs4 import BeautifulSoup
from selenium import webdriver

codechef_url = 'https://www.codechef.com/contests'
driver = webdriver.Chrome()
driver.get(codechef_url)
print('done')


class Contest(NamedTuple):
    id: str
    link: str
    name: str
    start_time: datetime
    end_time: datetime


def get_codechef_contests():
    driver.refresh()
    time.sleep(1)
    html = driver.page_source
    page = BeautifulSoup(html, 'lxml')

    table_html = page.find(id='present-contests-data')
    table_rows = table_html.find_all('tr')

    contests = []
    for tr in table_rows:
        td = tr.find_all('td')
        contest_id, name, start_time_str, end_time_str = td
        contest = Contest(
            contest_id.text,
            'https://www.codechef.com' + name.a['href'],
            name.text,
            datetime.strptime(start_time_str.text, "%d %b %Y  %H:%M:%S"),
            datetime.strptime(end_time_str.text, "%d %b %Y  %H:%M:%S"),
        )
        contests.append(contest)

    return contests


if __name__ == '__main__':
    while True:
        contests = get_codechef_contests()
        contests.sort(key=lambda contest: contest.start_time)

        if len(contests) == 0:
            print('nothing found')
            time.sleep(7200)
            continue

        nearest_contest = contests[0]
        while True:
            time.sleep(300)
            if nearest_contest.start_time - timedelta(hours=1) <= datetime.now():
                print(f'Contest {nearest_contest.name} starts in 1 hour')
                break
