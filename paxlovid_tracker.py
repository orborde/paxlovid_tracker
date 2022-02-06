#! /usr/bin/env python3

import argparse
import collections
from io import StringIO
import requests


parser = argparse.ArgumentParser()
parser.add_argument(
    "--webhook_url",
    help="Discord webhook URL to send to",
    required=True,
    )
parser.add_argument(
    "--coordinates",
    help="Lat/long to track availability near",
    type=str,
    default="47.6190262,-122.4031093",
)
parser.add_argument(
    "--radius",
    help="Radius to track availability in (meters)",
    type=int,
    default=2000,
)

args = parser.parse_args()

#     "$where=order_label='Paxlovid' and "+
data = requests.get(
    "https://healthdata.gov/resource/rxn6-qnx8.json?$where=" +
    "within_circle(geocoded_address, 47.6637325, -122.3446932, 10000)"
).json()

print(data)
COURSES_AVAILABLE_KEY = "courses_available"

courses_by_product = collections.defaultdict(list)
sites_by_product = collections.defaultdict(int)
for result in data:
    order_label = result["order_label"]
    sites_by_product[order_label] += 1
    if COURSES_AVAILABLE_KEY not in result:
        courses_by_product[order_label].append(0)
    else:
        courses_by_product[order_label].append(int(result[COURSES_AVAILABLE_KEY]))

content_string = StringIO()
print(f"**COVID-19 therapeutics available within {args.radius:,}m of {args.coordinates}:**", file=content_string)
for product in sorted(courses_by_product.keys()):
    courses_available = sum(courses_by_product[product])
    sites_available = sites_by_product[product]
    print(
        f"{product}: {courses_available}",
        f"({len(courses_by_product[product])}/{sites_available} sites reporting)",
        file=content_string,
    )

webhook_data = {
    "username":"TrackerBot",
    "content":content_string.getvalue(),
}

requests.post(args.webhook_url, json=webhook_data)