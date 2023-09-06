#!/usr/bin/python3
# -- coding: utf-8 --**
import json

from flask import Flask, request, jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer

from com.gitevents import *
from com.gittools import *
from com.logger import logger

monkey.patch_all()

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def sync_event(): 
    if 'X-Gitlab-Token' in request.headers.keys() \
            and request.headers['X-Gitlab-Token'].strip() == Config.webhook_token.strip():
        if len(request.data) <= 0:
            return jsonify({'status': 'bad content'}), 403
        event = json.loads(request.data)
        if isinstance(event, dict):
            event_deal(event)
        elif isinstance(event, list):
            for ent in event:
                event_deal(ent)
        else:
            logger.info('sync_event接收' + str(type(event)) + '类型event，无处理程序~')
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'bad token'}), 401


def event_listen():
    logger.info('....................开启webhook监听:' + str(Config.webhook_port) + '....................')
    WSGIServer(('0.0.0.0', Config.webhook_port), app).serve_forever()


if __name__ == '__main__':
    print('\n'.join(('%s:   %s' % item for item in Config.__dict__.items())))  
    event_listen()
