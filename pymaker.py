#!/usr/bin/env python3

import requests
import sys
import re
import time

MAIN_URL="https://api.github.com/search/repositories"

linkFinder = re.compile('^<(.*)>; rel="next"')

def main(org, token):
    """Prints the list of repos in a GitHub org in CSV format, with name and SSH URL fields

    Args:
        org (str): The org that you want to query
        token (str): Your GitHub API token
    """
    headers = {
        'Authorization': f"token {token}",
        'User-Agent': 'python'
    }
    params = { 'q': f"org:{org}"}
    url = MAIN_URL
    while(True):
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if 'items' not in data.keys():
            print(data)
            break

        for item in data['items']:
            print(f"{item['name']},{item['ssh_url']}")

        m = linkFinder.match(response.headers['Link'])

        if m: url = m[1]
        else: break
        # search API is limited to 30 queries per minute
        time.sleep(3)
        break

if __name__ == '__main__':
    main(*[x for x in sys.argv[1:]])
