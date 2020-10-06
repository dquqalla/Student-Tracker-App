from flask import url_for

# Configuration for url_for, add /usr/395 to the end of the URL
URL_PREFIX = '/usr/395'

def vs_url_for(view):
    url = url_for(view)
    url = URL_PREFIX + url
    return url


