#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from argparse import ArgumentParser
import re
import config


class HTMLExternalsParser(HTMLParser):
    # сюда записываются найденные css-ссылки
    css = []

    # сюда записываются найденные js-ссылки
    js = []

    @staticmethod
    def parse_link(link):
        if link and type(link) == str:
            return link.split('?')[0]

    @staticmethod
    def remove_resource_root(link, folder):
        return re.sub(folder, '', link)

    @staticmethod
    def check_tag_type(tag):
        for excluded_type in config.excluded_types:
            if excluded_type in tag:
                return False

        return True

    @staticmethod
    def is_external_link(link):
        return re.compile(r'(http|//)').search(link)

    def __str__(self):
        if not self.css or not self.js:
            return 'Отсутствуют подходящие ссылки'
        else:
            return '\n\n'.join(
                (
                    ' '.join(self.css),
                    ' '.join(self.js)
                )
            )

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'link'] and attrs and self.check_tag_type(attrs):
            for attr in attrs:
                link = self.parse_link(attr[1])

                if link and link not in config.excluded_links and not self.is_external_link(link):
                    if attr[0] == 'href':
                        self.css.append(self.remove_resource_root(link, '/css/'))
                    elif attr[0] == 'src':
                        self.js.append(self.remove_resource_root(link, '/js/'))


def get_args():
    arg_parser = ArgumentParser(description='HTML externals parser')
    arg_parser.add_argument(
        '-p',
        action='store',
        required=True,
        metavar='path_to_html_file',
        help='Path to file'
    )

    return arg_parser.parse_args()


if __name__ == '__main__':
    try:
        html_file = open(get_args().p).read()

        parser = HTMLExternalsParser()
        parser.feed(html_file)

        print(parser)
    except Exception as e:
        print(e)