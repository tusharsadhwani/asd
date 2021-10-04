#!/usr/bin/env zxpy
import json

import rich
from rich.table import Table

response = ~(
    "curl -s 'https://api.github.com/search/issues"
    "?q=author:tusharsadhwani"
    "+is:issue"
    "+is:open"
    "&per_page=100'"
)

data = json.loads(response)
user_name = data["items"][0]["user"]["login"]
issue_names = [issue["title"] for issue in data["items"]]

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Author")
table.add_column("Issue name", justify="right")

for issue_name in issue_names:
    table.add_row(user_name, issue_name)

rich.print(table)
