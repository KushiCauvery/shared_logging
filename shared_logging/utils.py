from rest_framework import status
from rest_framework.response import Response

from .logging import custom_log

def response(data, code=status.HTTP_200_OK, error="", request=None, to_log=True):
    """Overrides rest_framework response

        :param request:
        :param to_log:
        :param data: data to be send in response
        :param code: response status code(default has been set to 200)
        :param error: error message(if any, not compulsory)
    """
    res = {"error": error, "response": data}
    if to_log:
        custom_log('info', request=request, params={'body': res})
    return Response(data=res, status=code)