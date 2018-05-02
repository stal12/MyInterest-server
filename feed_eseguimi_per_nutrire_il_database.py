#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""FeedCollector

Usage:

    feedCollector -a <rss-url> -c <category>
    feedCollector -d <rss-url>
    feedCollector -t <category>
    feedCollector (-h | --help)
    feedCollector --topics
Options:
                                Start FeedCollector with while loop.
    -a URL  -c CATEGORY         Add new url <rss-url> to database under <category>
    -d URL                      Delete <rss-url> from the database file.
    -t CATEGORY                 Show the stored urls for the specific <category>.
    -h --help                   Show this screen.
    --topics                    Show all the stored topics
"""

from __future__ import print_function

import argparse
import os
import time

# import db
import django
from FeedCollector.myFeedParser import myFeedParser
from pony import orm

from FeedCollector.urls import rss

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyInterest.settings")
django.setup()

from server import models

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen



def _connected():
    """check internet connect"""
    host = 'http://google.com'

    try:
        urlopen(host)
        return True
    except:
        return False


def urls_populate_db(rss):
    for cat in rss.keys():
        if not models.Category.objects.filter(name=cat).exists():
            cat_obj = models.Category(name=cat)
            cat_obj.save()
        else:
            cat_obj = models.Category.objects.get(name=cat)
        for url in rss[cat]:
            if not models.Url.objects.filter(link=url).exists():
                url_obj = models.Url(link=url, category=cat_obj)
                url_obj.save()


def main():

    urls_populate_db(rss)

    # parser = argparse.ArgumentParser(description="esegue feedCollector")
    # parser.add_argument('-a', action="store", dest="a", help="add url A in category -c" )
    # parser.add_argument('-c', action="store", dest="c", help="category")
    # parser.add_argument('-d', action="store", dest="d", help="delete url B")
    # parser.add_argument('--topics', action="store_true", default=False, help="show all topics")
    # parser.add_argument('-t', action="store", dest="t", help="show urls topic T")
    #
    # args = parser.parse_args()
    # print(args)
    #
    # a = args.a
    # c = args.c
    # d = args.d
    # t = args.t
    # topics = args.topics
    #
    # #DB init
    #
    # flag_populated = os.path.isfile('../../db.sqlite3')  # true if existing
    #
    # if not flag_populated:
    #     mdb = db.define_database_and_entities(provider='sqlite', filename='../../db.sqlite3', create_db=False)
    #     # db.urls_populate_db(mdb, rss)
    #     print('db created and populated')
    # else:
    # mdb = db.define_database_and_entities(provider='sqlite', filename='../../db.sqlite3', create_db=False)
    #     print('db connected')
    #
    # db.urls_populate_db(mdb, rss)
    #
    # if a is not None:
    #
    #     if c is not None:
    #         mfp = myFeedParser(a, c)
    #         url = mfp.parseFeed()
    #
    #         if url is not None:
    #             with orm.db_session:
    #                 if not mdb.Url.exists(link=a):
    #                     url = mdb.Url(link=a, category=c)
    #                     mdb.commit()
    #                 else:
    #                     print('url already existing')
    #
    #         else:
    #             print('url not valid')
    #
    #     else:
    #         print('insert topic')
    #
    # elif d is not None:
    #
    #     with orm.db_session:
    #         if mdb.Url.exists(link=d):
    #
    #             link = mdb.Url[d]
    #             print(link)
    #             link.delete()
    #             mdb.commit()
    #             print('link {} deleted'.format(d))
    #         else:
    #             print('link not existing')
    #
    # elif t is not None:
    #     if t in rss.keys():
    #         with orm.db_session:
    #
    #             links = mdb.Url.select(lambda top:  top.category == t)
    #             for l in links:
    #                 print(l)
    #     else:
    #         print('topic {} not existing'.format(t))
    #
    # elif topics is True:
    #     print(rss.keys())
    #
    # else:
        #5 minutes
    timeout = 60*5
    while True:

        print("loop")
        urls = models.Url.objects.all()
        for url in urls:
            print(url.link)

        # populating items
        for top in rss.keys():
            cat = models.Category.objects.get(name=top)
            urls_topic_x = models.Url.objects.filter(category=cat)
            for l1 in urls_topic_x:

                fp = myFeedParser(url=l1.link, topic=top)
                correct = fp.parseFeed()
                if correct is not None:
                    print('feed {} ok'.format(fp.url))
                    list_item_parsed = fp.fetchFeed()
                    for it in list_item_parsed:
                        if models.Item.objects.filter(link=it['link']).exists():
                            continue
                        else:
                            models.Item(link=it['link'], title=it['title'], description=it['descr'], date=it['pubDate'], thumbnail=it['img'], category=cat).save()

                else:
                    print('feed not valid')

        print("timeout")
        time.sleep(timeout)


# start
if __name__ == '__main__':

    if not _connected():
        print('No Internet Connection!')
        exit()

    main()








