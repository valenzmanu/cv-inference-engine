from __future__ import print_function

import logging

from inference_engine.inference_engine import InferenceEngine
from receiver.receiver import Receiver

logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - [%(levelname)s] %(pathname)s:%(lineno)s -> %(message)s')

receiver_server = Receiver(InferenceEngine.make_inference, port=8181)
receiver_server.start()
