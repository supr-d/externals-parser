"""
HTMLResLinksParser config
"""

# Ссылки, которые не учитывать.
# Необходимо указывать такой же путь, как в src/href,
# без знака вопроса и последующих параметров
ignore_links = [
    '/css/map.min.css',
    '/css/index.min.css',
    '/js/map.min.js',
    '/js/index.min.js'
]

# Игнорировать внешние ссылки. Например: http://example.com/css/main.css
ignore_external_links = True


"""
SLON-parser config
"""

# путь к папке со starline-online без слэша в конце
project_root = '/home/a20824/www/debug0.starline.local/www'


# путь к файлу index.php относительно project_root со слэшем в начале
index_path = '/protected/views/layouts/index.php'

# пути к файлам css/js получаемых в результате сжатия
index_result_js_path = '/js/index.min.js'
index_result_css_path = '/css/index.min.css'


# путь к файлу map.php относительно project_root со слэшем в начале
map_path = '/map.php'

# пути к файлам css/js получаемых в результате сжатия
map_result_js_path = '/js/map.min.js'
map_result_css_path = '/css/map.min.css'