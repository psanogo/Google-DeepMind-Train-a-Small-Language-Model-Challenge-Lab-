from flask import Flask, render_template, request, url_for, redirect
import feedparser
from urllib.parse import quote, unquote
from datetime import datetime

app = Flask(__name__)

def get_feed():
    feed = feedparser.parse('data/feed.xml')
    for entry in feed.entries:
        # Convert pubDate string to datetime object for sorting
        entry.published_datetime = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
    # Sort entries from most recent to least recent
    feed.entries.sort(key=lambda e: e.published_datetime, reverse=True)
    return feed

@app.route('/')
def index():
    feed = get_feed()
    return render_template('index.html', entries=feed.entries, quote=quote)

@app.route('/entry')
def entry():
    guid = request.args.get('guid')
    feed = get_feed()
    found_entry = next((e for e in feed.entries if e.guid == guid), None)
    if not found_entry:
        return redirect(url_for('index'))
    return render_template('entry.html', entry=found_entry)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)