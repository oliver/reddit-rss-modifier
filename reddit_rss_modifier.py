#!/usr/bin/python

#
# CGI script for serving a modified Reddit RSS feed, where the linked-to article is contained in the <link> tag.
#

import sys
import os
import re
import cgi
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# only for debugging:
import cgitb
cgitb.enable()


def cgi_die(http_status, message):
    print "Status:%d\nContent-type: text/plain\n\n%s\n" % (http_status, message)
    sys.exit(1)


def modify_rss(orig):
    root = ET.fromstring(orig)
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        try:
            links = entry.findall("{http://www.w3.org/2005/Atom}link")
            contents = entry.findall("{http://www.w3.org/2005/Atom}content")
            if links and contents:
                real_link = None
                soup = BeautifulSoup(contents[0].text, "html.parser")
                for a_element in soup.find_all("a"):
                    if a_element.text == "[link]":
                        real_link = a_element.attrs["href"]
                        break
                if real_link:
                    links[0].attrib["href"] = real_link
        except:
            pass # cannot modify element; ignore error

    return '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(root)


if __name__ == "__main__":
    if "REQUEST_METHOD" in os.environ:
        # CGI mode
        form_params = cgi.FieldStorage()
        if not "topic" in form_params:
            cgi_die(400, "parameter \"topic\" is missing")
        topic = form_params["topic"].value
        if not(re.match(r"^[a-zA-Z0-9]+$", topic)):
            cgi_die(400, "parameter \"topic\" has invalid contents")
    else:
        # locally called
        topic = sys.argv[1]

    orig_url = "https://www.reddit.com/r/%s/.rss" % topic

    headers = {"User-agent": "reddit_rss_modifier/1.0"}
    r = requests.get(orig_url, headers=headers)
    if r.status_code != requests.codes.ok:
        cgi_die(400, "request for \"%s\" failed with code %s: %s" % (orig_url, r.status_code, r.text))
    orig_text = r.text.encode("utf-8")

    new_text = modify_rss(orig_text)

    print "Content-Type: application/atom+xml; charset=UTF-8\n"
    print new_text
