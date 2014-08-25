from html.parser import HTMLParser
import re


class HTMLResLinksParser(HTMLParser):
    def __init__(self, config):
        HTMLParser.__init__(self)
        self.css = []
        self.js = []
        self.config = config

    def __str__(self):
        if not self.css or not self.js:
            return u'Не найдено ни одной ресурсной ссылки'
        else:
            return '\n\n'.join(
                (' '.join(self.css), ' '.join(self.js))
            )

    @staticmethod
    def has_valid_attrs(attrs):
        """
        Возвращает True, если атрибуты содержат rel="stylesheet" или атрибут src

        :param attrs:
        :return boolean:
        """
        return ('rel', 'stylesheet') in attrs or [attr for attr in attrs if 'src' in attr]

    def check_link(self, link):
        """
        Возвращает True если переданная ссылка - не внешняя или отключена проверка и
        False если включена проверка и ссылка - внешняя

        :param link:
        :return boolean:
        """
        return not re.search(r'(http|//)', link) if self.config.ignore_external_links else True

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'link'] and self.has_valid_attrs(attrs):
            for attr in attrs:
                # пропускаем пустые ссылки
                if not attr[1]:
                    continue

                link = attr[1].split('?')[0]  # убираем все символы после знака "?"

                if link not in self.config.ignore_links and self.check_link(link):
                    if attr[0] == 'href':
                        self.css.append(link)
                    elif attr[0] == 'src':
                        self.js.append(link)
