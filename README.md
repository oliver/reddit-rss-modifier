# Reddit RSS Modifier

This CGI script serves a modified RSS feed for Reddit where the linked-to article is contained in the "link" tag.
With these modification an RSS feed reader will download the linked-to article, rather than the Reddit comments.

## Installation
- install Python and BeautifulSoup
- set up `reddit_rss_modifier.py` as CGI script on your webserver, eg. for a location like `/reddit-rss`
- access the RSS feed at an URL like this: `http://yourserver/reddit-rss?topic=someRedditTopic`

## Local Test Setup
You can run the script in a local Lighttpd web server with this command: `lighttpd -f lighttpd.conf -D`
Afterwards the CGI script is reachable at http://localhost:8089/?topic=someRedditTopic .

For debugging, you can also run the script from command line and pass the topic as command line parameter.
