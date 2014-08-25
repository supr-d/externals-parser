#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from HTMLResLinksParser.HTMLResLinksParser import HTMLResLinksParser
import config
import os


def abs_path(path):
    return config.project_root + path

if __name__ == '__main__':
    choice = input(u'Какой файл будем сжимать?\ni - index\nm - map\n')

    if choice == 'i':
        file_path = abs_path(config.index_path)
        css_result_file = abs_path(config.index_result_css_path)
        js_result_file = abs_path(config.index_result_js_path)
    elif choice == 'm':
        file_path = abs_path(config.map_path)
        css_result_file = abs_path(config.map_result_css_path)
        js_result_file = abs_path(config.map_result_js_path)
    else:
        print(u'Неправильный выбор :(')
        exit()

    try:
        parser = HTMLResLinksParser(config)
        parser.feed(open(file_path).read())

        print('\nКомпрессия CSS-файлов...\n')
        for css_file in parser.css:
            print('Компрессия %s' % css_file)
            os.system('yui-compressor {0} >> {1}'.format(abs_path(css_file), css_result_file))

        print('\nКомпрессия JS-файлов...\n')
        for js_file in parser.js:
            print('Компрессия %s' % js_file)
            os.system('yui-compressor {0} >> {1}'.format(abs_path(js_file), js_result_file))

        print('\nЗавершено')
    except FileNotFoundError as e:
        print(e.strerror)