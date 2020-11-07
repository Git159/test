# coding=utf-8
import requests
import time
from Queue import Queue
from lxml import etree
import gevent
import gevent.monkey

gevent.monkey.patch_all()
class ssr(object):
    def __init__(self):
        self.q = Queue()
        self.headers = {}

    def run(self, url):
        self.parse_page(url)

    def send_requests(self, url):
        i = 0
        while i <= 3:
            try:
                html = requests.get(url, headers=self.headers).content
            except Exception as e:
                print(r'error %s%s' % (url, e))
                i += 1
            else:
                return html

    def parse_page(self, url):
        response = self.send_requests(url)
        html = etree.HTML(response)
        movie_list = html.xpath('//div[2]/a/h2')
        for movie in movie_list:
            movie_name = movie.xpath('./text()')[0]
            # print(movie_name)
            self.q.put(movie_name)
    def main(self):
        base_url = 'https://ssr1.scrape.center/page/'
        url_list = [base_url + str(i) for i in range(1, 11)]
        l = len(url_list) / 2
        job_list = []
        job_list_1 = [gevent.spawn(self.run, url) for url in url_list[:l]]
        job_list_2 = [gevent.spawn(self.run, url) for url in url_list[l:l*2]]
        # job_list_3 = [gevent.spawn(self.run, url) for url in url_list[l*2:l*3]]
        # job_list_4 = [gevent.spawn(self.run, url) for url in url_list[l*3:l*4]]
        job_list.append(job_list_1)
        job_list.append(job_list_2)
        # job_list.append(job_list_3)
        # job_list.append(job_list_4)
        for i in job_list:
            gevent.joinall(i)
            time.sleep(10)
        # job_list = [gevent.spawn(self.run, url) for url in url_list]
        # gevent.joinall(job_list)
        while not self.q.empty():
            print(self.q.get())
if __name__ == '__main__':
    start = time.time()
    crawler = ssr()
    crawler.main()
    print('[info]耗时：%s' % (time.time() - start))
