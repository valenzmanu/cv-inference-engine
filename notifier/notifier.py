import logging
import threading
from queue import Queue

import requests


class Notifier(threading.Thread):

    def __init__(self, notify_to_url: str):
        super().__init__()
        self.notify_to_url: str = notify_to_url
        self.notification_queue = Queue()

    def queue_notification(self, content: dict):
        self.notification_queue.put(content)

    def notify(self, content: dict):
        logging.info("Sending %s to %s" % (str(content), self.notify_to_url))
        params = {'source': 'InferenceEngine'}
        r = requests.get(self.notify_to_url, json=content, params=params)
        logging.info("Received response from %s: %s" % (self.notify_to_url, str(r)))

    def run(self) -> None:
        while True:
            while not self.notification_queue.empty():
                notification = self.notification_queue.get()
                self.notify(notification)
