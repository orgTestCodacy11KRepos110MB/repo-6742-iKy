#!/usr/bin/env python

from __future__ import absolute_import

import sys
import requests
import json
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main(username):
    # Use the username variable to do some stuff and return the data
    gitlabdetails = []
    url = "https://gitlab.com/" + username
    if (requests.head(url, verify=False).status_code == 200):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        handle= soup.find("span", {"class" : "middle-dot-divider"})
        if handle:
            name= soup.find("div", {"class" : "cover-title"})
            gitlabdetails.append("Name: " +name.text.strip())
            handle= soup.find("span", {"class" : "middle-dot-divider"})
            mydivs = soup.findAll("div", { "class" : "profile-link-holder middle-dot-divider" })
            for div in mydivs:
                q=div.find('a', href=True)
                if q:
                  gitlabdetails.append(q['href'].strip())
                elif div.find("i", {"class" : "fa fa-map-marker"}):
                  gitlabdetails.append("Location:" + div.text.strip())
                elif div.find("i", {"class" : "fa fa-briefcase"}):
                  gitlabdetails.append("Organisation: " + div.text.strip())

    return gitlabdetails


def output(data):
    print json.dumps(data, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        result = main(username)
        output(result)
    except Exception as e:
        print e
        print "Please provide a username as argument"
