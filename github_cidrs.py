#!/usr/bin/env python3

import json
import requests
import sys

# Edit the following section to change script constants
CIDR_BLOCKS_REQUIRED = ["web","api"]
FILTER_IPV6 = True
GITHUB_API_URL = "https://api.github.com/meta"
TIMEOUT = 5

# Try to get response from Github API
try:
    github_response = requests.get(GITHUB_API_URL, timeout=TIMEOUT)
except requests.exceptions.RequestException as e:
    # Exception if it fails
    raise SystemExit(e) from e

# Check if response is 2xx
try:
    github_response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(str(e), file=sys.stderr)
    raise SystemExit(1) from e

cidr_list = []
for i in CIDR_BLOCKS_REQUIRED:
    if i in github_response.json():
        for x in github_response.json()[i]:
            if FILTER_IPV6:
                if not "::" in x:
                    cidr_list.append(x)
            else:
                cidr_list.append(x)

result = {
    "cidrs": cidr_list
}

print(json.dumps(result))
