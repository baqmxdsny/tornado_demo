from apps.foo.handlers.foo import FooHandler
from utils.urlparse import include, url_wrapper

url_patterns = url_wrapper([
    (r"/foo", include('apps.foo.urls')),
])
