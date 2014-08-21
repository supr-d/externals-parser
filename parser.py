#!/usr/local/bin/python3 -tt
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from argparse import ArgumentParser
import re
import config


class HTMLResLinksParser(HTMLParser):
    # сюда записываются найденные css-ссылки
    css = []

    # сюда записываются найденные js-ссылки
    js = []

    def __str__(self):
        if not self.css or not self.js:
            return 'Не найдено ни одной ресурсной ссылки'
        else:
            return '\n\n'.join(
                (' '.join(self.css), ' '.join(self.js))
            )

    @staticmethod
    def check_attrs(attrs):
        return ('rel', 'stylesheet') in attrs or [attr for attr in attrs if 'src' in attr]

    @staticmethod
    def remove_link_params(link):
        return link.split('?')[0]

    @staticmethod
    def is_external_link(link):
        return config.ignore_externals and re.compile(r'(http|//)').search(link)

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'link'] and self.check_attrs(attrs):
            for attr in attrs:
                param_name = attr[0]
                link = self.remove_link_params(attr[1])

                external_check = \
                    True if not config.ignore_externals \
                    else True if not self.is_external_link(link) \
                    else False

                if link not in config.ignore_links and external_check:
                    if param_name == 'href':
                        self.css.append(link)
                    elif param_name == 'src':
                        self.js.append(link)


def get_args():
    arg_parser = ArgumentParser(description='HTML resource links parser')
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
        target_file = open(get_args().p).read()

        parser = HTMLResLinksParser()
        parser.feed(target_file)

        print(parser)
    except Exception as e:
        print(e)