import logging
import json
from inspect import getframeinfo, stack
from datetime import datetime, date, time

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request

logger = logging.getLogger("default")

#new version
class DatetimeEncoder(json.JSONEncoder):
    """
    for making datetime and date object serializable
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%I:%M %p')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def warning(params, access_token="", agent_code="", source_code="", file_name ="", line_no=""):
    """
    logs with level warning
    :param: access_token: access_token of the user
    :param: params: dict of the data to be logged
    """
    logger.warning(access_token + ' || ' + agent_code + ' || ' + source_code + ' || ' + file_name + ' || ' + line_no + ' || ' + params)


def debug(params, access_token="", agent_code="", source_code="", file_name ="", line_no=""):
    """
    logs with level debug
    :param: access_token: access_token of the user
    :param: params: dict of the data to be logged
    """
    logger.debug(access_token + ' || ' + agent_code + ' || ' + source_code + ' || ' + file_name + ' || ' + line_no + ' || ' + params)


def info(params, access_token="", agent_code="", source_code="", file_name ="", line_no=""):
    """
    logs with level info
    :param: access_token: access_token of the user
    :param: params: dict of the data to be logged
    """
    logger.info(access_token + ' || ' + agent_code + ' || ' + source_code + ' || ' + file_name + ' || ' + line_no + ' || ' + params)


def error(params, access_token="", agent_code="", source_code="", file_name ="", line_no=""):
    """
    logs with level error
    :param: access_token: access_token of the user
    :param: params: dict of the data to be logged
    """
    logger.exception(access_token + ' || ' + agent_code + ' || ' + source_code + ' || ' + file_name + ' || ' + line_no + ' || ' + params)


def custom_log(level, request=None, params=None):
    """
    logs on the logfile
    :param: level:level name of logging(warn,debug,info or error)
    :param: access_token: access_token of the user
    :param: params: dict of the data to be logged
    """
    try:
        access_token = ""
        agent_code = ""
        source_code = ""
        if request and isinstance(request, Request):
            if request.auth:
                access_token = request.auth.token
            if hasattr(request, 'hash_trace'):
                params['hash_trace'] = request.hash_trace
            if not params:
                params = {'myurl': request.path}
            else:
                params.setdefault('myurl', request.path)
            agent_code = request.META.get('HTTP_AGENT_CODE', "")
            source_code = request.META.get('HTTP_SOURCE_CODE', "")
        elif request and isinstance(request, WSGIRequest):
            access_token_meta = request.META.get('HTTP_AUTHORIZATION', " ").split(" ")
            access_token = "" if len(access_token_meta) != 2 else access_token_meta[1]
            agent_code = request.META.get('HTTP_AGENT_CODE', "")
            source_code = request.META.get('HTTP_SOURCE_CODE', "")
            if hasattr(request, 'hash_trace'):
                params['hash_trace'] = request.hash_trace
            if not params:
                params = {'myurl': request.path}
            else:
                params.setdefault('myurl', request.path)
            params.setdefault('headers', str(request.META))
        elif request:
            access_token = request.get('token', "")
            agent_code = request.get('HTTP_AGENT_CODE', "")
            source_code = request.get('HTTP_SOURCE_CODE', "")
            params['hash_trace'] = request.get('hash_trace')
        options = {
            'warn': warning, 'debug': debug, 'info': info, 'error': error
        }
        caller = getframeinfo(stack()[1][0])
        file_name = str(caller.filename)
        line_no = str(caller.lineno)
        options[level](json.dumps(params, cls=DatetimeEncoder), access_token, agent_code, source_code, file_name, line_no)
    except Exception as e:
        print("Error while logging")
        print(repr(e))
