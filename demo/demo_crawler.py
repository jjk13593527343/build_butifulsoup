# coding:utf-8

import json
import time
from scpy2 import util
from scpy2.crawlers.crawler import Crawler


class DemoCrawler(Crawler):
    def _run(self, params):

        cp = self._load_crawl_processor()

        data = cp.crawl()
        self.send(data)


    def send (self):
        print("im here!")
    

if __name__ == '__main__':
    # import sys

    worker = DemoCrawler()
    # print worker.work_path
    # sys.path.append(worker.work_path+'/crawlers')
    worker.run()
