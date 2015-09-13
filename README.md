# What is CrawleMe! ?

CrawleMe! is is easy way of crawling image or link urls from any web site.

# How It Works ?
Create your web page wrapper class.
```python
from crawleme.base import BasePage

class MyPage(BasePage):
	url = 'http://www.mysite.com'
	item_path = '//*[@id="campaign_list"]/div/a'
	item_attribute = 'href'
```

Create a instance of wrapper class and call crawle method.
```python
crawler = MyPage()
urls = crawler.crawle()

for url in urls:
	print url
```

Result:
```
http://www.mysite.com/id/5
http://www.mysite.com/aboutus/
http://www.mysite.com/foo/
http://www.mysite.com/bar/
http://www.mysite.com/baz/
```

Also, you can pass or override the url or item_path of wrapper class on creating class instance.
```python
crawler = MyPage(url='http://www.mysite.com/id/112312')
```

# Properties:
**url:** <br />
Url of page that will be crawled. <br/>
<br/>
**item_path:**<br/>
X-Path of selected DOM element(s).
<br/>
<br/>
**item_attribute:**<br/>
Attribute of selected DOM element(s).
<br/>
<br/>
**has_only_single_item:**<br/>
crawle method returns only single value when there is True
<br/>
<br/>
**fix_urls:**<br/>
Sometimes may be DOM object attributes contains only path value without hostname and protocol. This attributes fix the parsed value as full url.
<br/>
<br/>

# Methods:
**crawle([timeout=crawleme.conf.REQUEST_TIMEOUT],[renew=False]):**<br/>
Parses value list or single value from the page by the specified attributes.
<br/>
<br/>

**get_filename([timeout=crawleme.conf.REQUEST_TIMEOUT]):**<br/>
Returns requested filename.
<br/>
<br/>

**read([timeout=crawleme.conf.REQUEST_TIMEOUT]):**<br/>
read data from stream.
<br/>
<br/>