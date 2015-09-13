import urllib2
from lxml import html
from urlparse import urlparse

from .conf import REQUEST_TIMEOUT, USER_AGENT, CHUNK_SIZE
from .exceptions import RuntimeError, ConfigurationError


class BasePage(object):
    def __init__(self, url=None, item_path=None, item_attribute=None,
                 has_single_item=None, fix_urls=None):
        self.validate()
        self.prepare_settings(
            url, item_path, item_attribute, has_single_item, fix_urls)
        self.content = None
        self.handler = None

    def prepare_settings(self, url, item_path, item_attribute,
                         has_single_item, fix_urls):
        self.url = url or getattr(
            self, 'url')
        self.item_path = item_path or getattr(
            self, 'item_path')
        self.item_attribute = item_attribute or getattr(
            self, 'item_attribute')
        self.has_single_item = has_single_item or getattr(
            self, 'has_single_item', False)
        self.fix_urls = fix_urls or getattr(
            self, 'fix_urls', True)

    def validate(self):
        if not hasattr(self, 'url'):
            raise ConfigurationError('url is not set.')
        if hasattr(self, 'item_path') and not hasattr(self, 'item_attribute'):
            raise ConfigurationError('item_attribute is not set.')
        return True

    def build_request_header(self):
        return dict(
            [('User-Agent', USER_AGENT)])

    def fetch_content(self, timeout=REQUEST_TIMEOUT, is_stream=False):
        request = urllib2.Request(
            self.url, headers=self.build_request_header())
        self.handler = urllib2.urlopen(request, timeout=timeout)
        if is_stream:
            return self.handler
        else:
            self.content = self.handler.read()
            return self.content

    def get_base_url(self):
        parsed_url = urlparse(self.url)
        return '%s://%s' % (parsed_url.scheme, parsed_url.hostname)

    def fix_urls(self, url):
        if not self.fix_urls or not url:
            return None
        if url.startswith('http') or url.startswith('https'):
            return url
        else:
            return '%s%s' % (self.get_base_url(), url)

    def iterate(self, items):
        for item in items:
            value = self.fix_urls(item.get(self.item_attribute))
            if not value:
                continue
            yield value

    def parse_content(self):
        items = html.fromstring(self.content).xpath(self.item_path)
        if not self.has_single_item:
            return self.iterate(items)
        else:
            if not items:
                return None
            item = items[0]
            return self.fix_urls(item.get(self.item_attribute))

    def crawle(self, renew=False, timeout=REQUEST_TIMEOUT):
        if renew or self.content is None:
            self.fetch_content(timeout=timeout)
        if self.item_path and self.item_attribute:
            return self.parse_content()

    def get_filename(self, timeout=REQUEST_TIMEOUT):
        if not self.handler:
            self.fetch_content(timeout=timeout, is_stream=True)
        headers = self.handler.info().getheaders('Content-Disposition')
        if not headers:
            return None
        return headers[0]

    def read(self, size=CHUNK_SIZE, timeout=REQUEST_TIMEOUT):
        if not self.handler:
            self.fetch_content(timeout=timeout, is_stream=True)
        return self.handler.read(CHUNK_SIZE)
