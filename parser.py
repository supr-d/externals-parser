#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from argparse import ArgumentParser
import re


class HTMLExternalsParser(HTMLParser):
    files = {
        'css': [],
        'js': []
    }

    exception_links = [
        '/favicon.ico',
        '/css/map.min.css',
        '/js/map.min.js',
        'https://enterprise.api-maps.yandex.ru/2.0.37/'
    ]

    exception_types = [
        ('type', 'image/x-icon'),
        ('type', 'text/html')
    ]

    tags_to_scan = [
        'script',
        'link'
    ]

    @staticmethod
    def parse_link(link):
        return link.split('?')[0]

    @staticmethod
    def remove_root(link, folder):
        return re.sub(folder, '', link)

    def check_tag_types(self, tag):
        for val in self.exception_types:
            if val in tag:
                return False

        return True

    def handle_starttag(self, tag, attrs):
        if tag in self.tags_to_scan and attrs and self.check_tag_types(attrs):
            for attr in attrs:
                link = self.parse_link(attr[1])

                if link not in self.exception_links:
                    if attr[0] == 'href':
                        self.files['css'].append(self.remove_root(link, '/css/'))
                    elif attr[0] == 'src':
                        self.files['js'].append(self.remove_root(link, '/js/'))


def get_args():
    parser = ArgumentParser(description='HTML externals parser')
    parser.add_argument(
        '-p',
        action='store',
        required=True,
        metavar='path_to_html_file',
        help='Path to file'
    )

    return parser.parse_args()


if __name__ == '__main__':
    try:
        html_file = open(get_args().p).read()

        parser = HTMLExternalsParser()
        parser.feed(html_file)

        css_files = []
        js_files = []

        for css in parser.files['css']:
            css_files.append(css)

        print(' '.join(css_files))
        print()

        for js in parser.files['js']:
            js_files.append(js)

        print(' '.join(js_files))
    except Exception as e:
        print(e)