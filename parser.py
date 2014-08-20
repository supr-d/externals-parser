#!/Users/Dima/py/VirtualEnv/compressor-parser/bin/python -tt
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from argparse import ArgumentParser


class HTMLExternalsParser(HTMLParser):
    files = {
        'css': [],
        'js': []
    }

    @staticmethod
    def parse_link(link):
        return link.split('?')[0]

    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'link':
            for attr in attrs:
                if attr[0] == 'href':
                    self.files['css'].append(self.parse_link(attr[1]))
                elif attr[0] == 'src':
                    self.files['js'].append(self.parse_link(attr[1]))


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

        print(parser.files)
    except Exception as e:
        print(e)