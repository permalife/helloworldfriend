from __future__ import absolute_import
from hwf.celeryhwf.celery import app
from celery.utils.log import get_task_logger

import datetime

logger = get_task_logger(__name__)


@app.task
def greet_friend(name):
    """
    Celery task for greeting by name. Just adds the greeting to the logs for now
    and returns the execution timestamp.
    """
    logger.info('Hello %s' % name)
    return datetime.datetime.now()
