from multiprocessing import Pool, Manager
from Queue import Empty

from crawleme.base import BasePage
import sys, os

PROCESS_COUNT = 10
REQUEST_TIMEOUT = 10
QUEUE_TIMEOUT = 30
BASE_URL = 'http://www.mysite.com'


class MySitePage(BasePage):
    url = BASE_URL
    item_path = '(//body//a)'
    item_attribute = 'href'


def start_crawling(url, queue, visited_pages):
    try:
        crawler = MySitePage(url=url)
        urls = list(crawler.crawle(timeout=REQUEST_TIMEOUT))
        if not urls:
            return False
        for _url in urls:
            if _url in visited_pages or not _url.startswith(BASE_URL):
                continue
            visited_pages.append(_url)
            print _url
            queue.put(_url)
    except Exception, err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, err, fname, exc_tb.tb_lineno)


def process_queue(queue, pool, visited_pages):
    while True:
        try:
            url = queue.get(timeout=QUEUE_TIMEOUT)
            pool.apply_async(start_crawling, [url, queue, visited_pages])
        except Empty:
            break


if __name__ == '__main__':
    pool = Pool(processes=PROCESS_COUNT)
    manager = Manager()
    queue = manager.Queue()
    visited_pages = manager.list()
    pool.apply_async(start_crawling, [BASE_URL, queue, visited_pages])
    process_queue(queue, pool, visited_pages)
    pool.close()
    pool.join()