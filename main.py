from __future__ import print_function

import logging

from inference_engine.inference_engine import InferenceEngine
from notifier.notifier import Notifier
from receiver.receiver import Receiver

logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - [%(levelname)s] %(filename)s:%(lineno)s -> %(message)s')

notifier = Notifier(notify_to_url="http://localhost:8000/inference-result-processor")
inference_engine = InferenceEngine(inference_callback=notifier.queue_notification)
receiver_server = Receiver(inference_engine.queue_img, port=8181)

notifier.start()
inference_engine.start()
receiver_server.start()
