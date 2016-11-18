#!/usr/bin/env python

import os
import random
import requests
import subprocess
import argparse
import datetime

with open(os.path.expanduser('~/.flickr_api_key'), 'r') as key_file:
    FLICKR_API_KEY = key_file.readline().rstrip()

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class Config(AttrDict):
    def randomize(self):
        self.m = random.choice([1, 5, 6, 7, 8])
        self.n = random.randint(15, 60) * 10
        self.rep = 0
        self.a = 128
        self.r = 300
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
            self.a = 0
            self.n = random.randint(500, 2000)
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

def filter_by_aspect_ratio(photo_ids, min_ratio, max_ratio):
    url = 'https://api.flickr.com/services/rest/'

    def check_photo(p):
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
        if not thumbnail:
            return False

        ratio = float(thumbnail[0]['width']) / float(thumbnail[0]['height'])

        return ratio >= min_ratio and ratio <= max_ratio

    return filter(check_photo, photo_ids)

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

def primitive(**kwargs):
    args = []
    for k, v in kwargs.items():
        if v is None:
            continue
        args.append('-%s' % k)
        args.append(str(v))
    args = ' '.join(args)
    cmd = '/usr/local/bin/primitive %s' % args
    subprocess.call(cmd, shell=True)


def create_wallpaper(args):
    try:
        photos = filter_by_aspect_ratio(interesting(date=random_date()), 4.0/3.1, 22.0/9)
        photo = random.choice(photos)
        url = photo_url(photo, 'z')
        download_path = os.path.join('/tmp', photo['id'] + '.png')
        download_photo(url, download_path)

        output_path = os.path.expanduser(args.output)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        config = Config()
        config.randomize()
        config.validate()

        primitive(i=download_path,
                  s=args.size,
                  o='\'{0}\''.format(os.path.join(output_path, photo['id'] + '.png')),
                  **config)
    except Exception as e:
        print e

    finally:
        if os.path.exists(download_path):
            os.remove(download_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help="path to output directory", required=True)
    parser.add_argument('-s', '--size', type=int, help="width of output image", required=True)
    parser.add_argument('-n', '--num', type=int, help="number of wallpapers to generate", default=1)
    args = parser.parse_args()

    for n in xrange(args.num):
        create_wallpaper(args)

