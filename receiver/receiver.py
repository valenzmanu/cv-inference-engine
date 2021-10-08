import logging
import threading

from gevent import pywsgi
from requests_toolbelt.multipart import decoder


class Receiver:

    def __init__(self, handle_on_request, port: int, ip: str = 'localhost'):
        logging.debug("Initializing Receiver module")
        self.handle_on_request = handle_on_request
        self.server = pywsgi.WSGIServer((ip, port), self.handle)

    def start(self):
        self.server.serve_forever()

    def handle(self, env, start_response):
        # logging.debug(env)
        content_type = env.get('CONTENT_TYPE')
        content = env.get('wsgi.input').read(int(env.get('CONTENT_LENGTH', '0')))
        parts = decoder.MultipartDecoder(content, content_type)

        lst = []
        for part in parts.parts:
            disposition = part.headers[b'Content-Disposition']
            params = {}
            for disposition_part in str(disposition).split(';'):
                kv = disposition_part.split('=', 2)
                params[str(kv[0]).strip()] = str(kv[1]).strip('\"\'\t \r\n') if len(kv) > 1 else str(kv[0]).strip()
            _type = part.headers[b'Content-Type'] if b'Content-Type' in part.headers else None
            lst.append({'content': part.content, "type": _type, "params": params})
            for item in lst:
                name = item.get("params").get("name")
                data = item.get('content')
                thread = threading.Thread(target=self.handle_on_request, args=(data, name))
                thread.start()

        start_response('200 OK', [('Content-Type', 'text/html')])
        response = {'success': True}
        return [str(response).encode()]
