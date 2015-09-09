import urllib2
from lxml import html
from urlparse import urlparse

from .conf import REQUEST_TIMEOUT, USER_AGENT
from .exceptions import RuntimeError, ConfigurationError


class BasePage(object):
    def __init__(self, url=None, item_path=None):
        self.validate()
        if url is not None:
            self.url = url
        if item_path is not None:
            self.item_path = item_path
        self.content = None
        self.handler = None

    def validate(self):
        if not hasattr(self, 'url'):
            raise ConfigurationError('url is not set.')
        if not hasattr(self, 'item_path'):
            raise ConfigurationError('item_path is not set.')
        if not hasattr(self, 'item_attribute'):
            raise ConfigurationError('item_attribute is not set.')
        return True

    def build_request_header(self):
        return dict(
            [('User-Agent', USER_AGENT)])

    def fetch_content(self, timeout=REQUEST_TIMEOUT):
        request = urllib2.Request(self.url, headers=self.build_request_header())
        self.handler = urllib2.urlopen(request, timeout=timeout)
        self.content = self.handler.read()
        return self.content

    def get_base_url(self):
        parsed_url = urlparse(self.url)
        return '%s://%s' % (parsed_url.scheme, parsed_url.hostname)

    def parse_content(self):
        items = html.fromstring(self.content).xpath(self.item_path)
        for item in items:
            item_value = item.get(self.item_attribute)
            if not item_value:
                continue
            yield (item_value.startswith('http') or
                   item_value.startswith('https')) and \
                item_value or '%s%s' % (self.get_base_url(), item_value)

    def crawle(self, renew=False, timeout=REQUEST_TIMEOUT):
        if renew or self.content is None:
            self.fetch_content(timeout=timeout)
        return self.parse_content()

