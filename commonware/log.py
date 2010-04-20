import logging

from django.utils.thread_support import currentThread


_requests = {}


def get_remote_addr():
    return _requests.get(currentThread())


def set_remote_addr(addr):
    _requests[currentThread()] = addr


class ThreadRequestMiddleware(object):
    """
    Store the current remote address in thread-local storage so our
    logging wrapper can access it.
    """

    def process_request(self, request):
        set_remote_addr(request.META.get('REMOTE_ADDR', ''))


def getLogger(name):
    """
    Our own getLogger to return our logging wrapper around
    logging.Logger.
    """
    return CommonLogger(name)


class CommonLogger(logging.Logger):
    """
    A wrapper for logging.Logger that adds the IP address to every logged
    message.
    """
    
    def _get_extra(self):
        return {'REMOTE_ADDR': get_remote_addr(),}

    def info(self, msg, *args):
        logging.Logger.info(self, msg % args, extra=self._get_extra())

    def debug(self, msg, *args):
        logging.Logger.debug(self, msg % args, extra=self._get_extra())

    def warn(self, msg, *args):
        logging.Logger.warn(self, msg % args, extra=self._get_extra())

    def error(self, msg, *args):
        logging.Logger.error(self, msg % args, extra=self._get_extra())

    def exception(self, msg, *args):
        logging.Logger.exception(self, msg % args, extra=self._get_extra())

    def critical(self, msg, *args):
        logging.Logger.exception(self, msg % args, extra=self._get_extra())
