# coding: utf-8
import pyramid.httpexceptions as exc
from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(request):
        token = request.registry.settings.get('admintoken', None)
        giventoken = request.GET.get('admintoken', None)
        if giventoken != token:
            raise exc.HTTPUnauthorized('Invalid admin token')
        result = func(request)
        return result
    return wrapper


class LogHistoryChange(object):
    def __init__(self, document_type, event_type):
        self.document_type = document_type
        self.event_type = event_type

    def __call__(self, fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            # view func call
            result = fn(*args, **kwargs)
            # view func post-processing
            if self.event_type in ['update', 'delete', 'post'] and result:
                pid = result.get('code', None)
                collection = result.get('collection', None)
                log_data = {
                    'document_type': self.document_type,
                    'event': self.event_type,
                    'pid': pid,
                    'collection': collection,
                }
                db_broker = args[0]
                db_broker._log_changes(**log_data)

            # return view func response
            return result
        return decorated
