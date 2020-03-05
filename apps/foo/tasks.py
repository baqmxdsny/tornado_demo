#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-02-29 18:08
# @Software: PyCharm
# @File:     tasks.py

import time

from celery import Celery

app = Celery("tasks", broker="amqp://guest:guest@localhost:5672")
app.conf.CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672"

@app.task
def sleep_fun(second):
    time.sleep(second)
    return 'ok'

