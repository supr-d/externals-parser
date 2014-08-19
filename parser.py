#!/Users/Dima/py/VirtualEnv/compressor-parser/bin/python -tt
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from argparse import ArgumentParser
import sys


class CompressorHTMLParser(HTMLParser):
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
    parser = ArgumentParser(description='Compressor HTML parser')
    parser.add_argument('f', action='store', help='First fraction, e.g. 1/2')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', dest='add', action='store_true', help='Adds fractions')
    group.add_argument('-s', dest='sub', action='store_true', help='Subtracts fractions')
    group.add_argument('-m', dest='mul', action='store_true', help='Multiplies fractions')
    group.add_argument('-d', dest='div', action='store_true', help='Divides fractions')

    return parser.parse_args()


if __name__ == '__main__':
    html_file = open('index.html').read()

    parser = CompressorHTMLParser()
    parser.feed(html_file)

    # print(parser.files)

    args = get_args()