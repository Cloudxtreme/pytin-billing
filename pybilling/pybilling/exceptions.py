from __future__ import unicode_literals

import traceback

from pybilling.settings import logger


class ExceptionMiddleware(object):
    def process_exception(self, request, exception):
        logger.error(traceback.format_exc())
        return
