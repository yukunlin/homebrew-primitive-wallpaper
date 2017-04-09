#!/usr/bin/env python

import os
import random
import requests
import subprocess
import argparse
import datetime
import time
import sys

"""Based off https://github.com/fogleman/primitive/blob/master/bot/main.py
"""

with open(os.path.expanduser('~/.flickr_api_key'), 'r') as key_file:
    FLICKR_API_KEY = key_file.readline().rstrip()


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Config(AttrDict):
    def randomize(self):
        self.m = random.choice([1, 5, 7])
        self.n = random.randint(15, 50) * 10
        self.rep = 0
        self.a = 128
        self.r = 256

    def parse(self, text):
        text = (text or '').lower()
        tokens = text.split()
        for i, name in enumerate(MODE_NAMES):
            if name in text:
                self.m = i
        for token in tokens:
            try:
                self.n = int(token)
            except Exception:
                pass

    def validate(self):
        self.m = clamp(self.m, 0, 8)
        if self.m == 6:
            self.n = random.randint(1400, 2000)

    @property
    def description(self):
        total = self.n + self.n * self.rep
        return '%d %s' % (total, MODE_NAMES[self.m])


def clamp(x, lo, hi):
    if x < lo:
        x = lo
    if x > hi:
        x = hi
    return x


def random_date(max_days_ago=1000):
    today = datetime.date.today()
    days = random.randint(1, max_days_ago)
    d = today - datetime.timedelta(days=days)
    return d.strftime('%Y-%m-%d')


def interesting(date=None):
    url = 'https://api.flickr.com/services/rest/'
    params = dict(
        api_key=FLICKR_API_KEY,
        format='json',
        nojsoncallback=1,
        method='flickr.interestingness.getList',
    )
    if date:
        params['date'] = date
    r = requests.get(url, params=params)
    return r.json()['photos']['photo']


def get_aspect_ratio(p):
    url = 'https://api.flickr.com/services/rest/'
    params = dict(
        api_key=FLICKR_API_KEY,
        format='json',
        nojsoncallback=1,
        method='flickr.photos.getSizes',
        photo_id=p['id']
    )
    r = requests.get(url, params=params)
    sizes = r.json()['sizes']['size']
    thumbnail = filter(lambda x: x['label']=='Thumbnail', sizes)

    return float(thumbnail[0]['width']) / float(thumbnail[0]['height'])


def photo_url(p, size=None):
    # See: https://www.flickr.com/services/api/misc.urls.html
    if size:
        url = 'https://farm%s.staticflickr.com/%s/%s_%s_%s.jpg'
        return url % (p['farm'], p['server'], p['id'], p['secret'], size)
    else:
        url = 'https://farm%s.staticflickr.com/%s/%s_%s.jpg'
        return url % (p['farm'], p['server'], p['id'], p['secret'])


def download_photo(url, path):
    r = requests.get(url)
    with open(path, 'wb') as fp:
        fp.write(r.content)


def primitive(primitive_path, **kwargs):
    args = []
    for k, v in kwargs.items():
        if v is None:
            continue
        args.append('-%s' % k)
        args.append(str(v))
    args = ' '.join(args)
    cmd = '{0} {1}'.format(primitive_path, args)
    subprocess.call(cmd, shell=True)


def create_wallpaper(args):
    download_path = None

    try:
        print 'Finding interesting photo...'
        photos = interesting(date=random_date())
        photo = random.choice(photos)
        aspect_ratio = get_aspect_ratio(photo)

        print 'Downloading photo...'
        url = photo_url(photo, 'z')
        download_path = os.path.join('/tmp', photo['id'] + '.png')
        download_photo(url, download_path)

        output_path = os.path.expanduser(args.output)
        output_path = os.path.join(output_path, 'landscape' if aspect_ratio > 1 else 'portrait')
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        config = Config()
        config.randomize()
        config.validate()

        print 'Generating wallpaper with parameters {0}'.format(config)
        primitive(args.primitive_path,
                  i=download_path,
                  s=args.size,
                  o='\'{0}\''.format(os.path.join(output_path, photo['id'] + '.png')),
                  **config)
        print 'Done!'
    except Exception as e:
        print e

    finally:
        if download_path is not None and os.path.exists(download_path):
            os.remove(download_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help="path to output directory", required=True)
    parser.add_argument('-s', '--size', type=int, help="width of output image", required=True)
    parser.add_argument('--primitive_path', help="path to primitive executable", default='/usr/local/bin/primitive')
    parser.add_argument('-n', '--num', type=int, help="number of wallpapers to generate", default=1)
    args = parser.parse_args()

    # check network status
    max_retries = 10
    attempt = 0
    response = None

    while attempt < max_retries:
        attempt += 1
        try:
            print 'Checking network...'
            response = interesting()
            break
        except:
            print 'No network, retrying...'
            time.sleep(5)

    if response is None:
        print 'No network connection'
        sys.exit(1)

    for n in xrange(args.num):
        create_wallpaper(args)

