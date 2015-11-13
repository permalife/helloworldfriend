# Celery configuration file
from __future__ import absolute_import
from celery import Celery

app = Celery('hwf.celeryhwf',
             broker='amqp://',
             backend='amqp://',
             include=['hwf.celeryhwf.tasks'])

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
