from datetime import datetime
from time import mktime

import feedparser

from news.models import Feed, FeedLink
from newshub.celery import app

__all__ = ["update_feeds"]


@app.task
def update_feeds():
    for feed in Feed.objects.all():
        data = feedparser.parse(feed.url)
        for entry in data.entries:
            print(entry)
            FeedLink.objects.get_or_create(
                feed=feed,
                title=entry.title,
                description=entry.description,
                url=entry.link,
                date_published=datetime.fromtimestamp(mktime(entry.published_parsed)),
            )
        feed.last_feed_update = datetime.now()
        feed.save()
    return True
