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

Also, you can override url and item_path of wrapper class on creating class instance.
```python
crawler = MyPage(url='http://www.mysite.com/id/112312')
```
