# -*- coding: utf-8 -*-
import requests
import json
from multiprocessing import Pool
import time
import os
import sys


def send(data, url, key):
    print data
    os._exit()


class Sender(object):

    def __init__(self, batch_size=1):
        self.queue = []
        self.sending = []
        self.batch_size = batch_size
        self.url = os.environ.get('PYTILT_URL', None)
        self.key = os.environ.get('PYTILT_KEY', None)

    def add_data(self, data):
        self.queue.append(data)
        if len(self.queue) >= self.batch_size:
            self.send()

    def send(self):
        pool = Pool(processes=1)
        self.sending = list(self.queue)
        self.queue = []
        result = pool.apply_async(send, args=[self.sending, self.url, self.key], callback=self.completed)
        pool.close()
        pool.join()

    def completed(self, was_sent):
        if was_sent:
            self.sending = []
        else:
            if len(self.queue) > 100:
                self.queue = []
            self.queue += self.sending
