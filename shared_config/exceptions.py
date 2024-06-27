import logging
import json
from datetime import datetime
import pystache
import subprocess
from rest_framework.exceptions import APIException
from .external_utils import encrypt_response_json
from .renderer_constants import APP_OS
from .models import AppConfigurations
from . import settings
from .exception_constants import *
from . import constants as api_constants
from .logging import custom_log

logger = logging.getLogger("default")


def log_to_exception(status_type, exception_type, code, exception_code, detail, headers, body, url, is_popup,
                 specific_details, request):
    """
    Logs the following data to mongodb:
    - status_type : Email, CP, TEBT etc
    - exception_type : Retryable or NonRetryable
    - code : HTTP status code of the request which failed
    - exception_code : like SMS_UNREACHABLE or EMAIL_FAILURE
    - detail : The message used when generating the exception
    - headers : request headers if present
    - body : dump of request.body or request params
    - url : The url which was hit in case o third party failure, django url in case of internal exception
    - is_popup :
    - specific_details : dict which contains app_no, quote_id, tebt_quote_id, txn_id, combo_cc_quote_id
    """
    try:
        data_to_log = {
            "status_type": status_type,
            "exception_type": exception_type,
            "code": code,
            "exception_code": exception_code,
            "detail": detail,
            "headers": str(headers),
            "body": body,
            "myurl": url,
            "is_popup": is_popup
        }
        data_to_log.update(specific_details)
        custom_log("error", request, data_to_log)
    except:
        logger.info("Error while writing exception details to mongodb")


def parse_request_body(body):
    try:
        return json.dumps(body)
    except Exception:
        return json.dumps("")


class GenericException(APIException):
    detail = None
    exception_code = None
    status_code = 400  # User will always see Bad request 400 HTTP status code
    exception_type = EXCEPTION_TYPE_NON_RETRYABLE

    def __init__(self, status_type, exception_code, detail, masked_data=False, response=None, response_msg='', request=None, http_code=400, headers=None,
                 body=None, url=None, is_popup=True, specific_details={}, error_description_code='', to_be_encrypted=False):
        self.exception_code = exception_code
        if response_msg:
            response_msg = get_generic_error_message(headers, response_msg, request)
            self.response_msg = response_msg
        self.is_popup = is_popup
        if type(detail) != str:
            detail = detail.get('detail', '')
        if response_msg and not settings.DEBUG:
            self.detail = {"detail": response_msg, "is_popup": is_popup,
                           "error_description_code": error_description_code}
        else:
            self.detail = {"detail": detail, "is_popup": is_popup, "error_description_code": error_description_code}
        if exception_code in RETRYABLE_CODE.values():
            self.exception_type = EXCEPTION_TYPE_RETRYABLE
        if to_be_encrypted and self.detail:
            self.detail = {'data': encrypt_response_json(None, self.detail)}
        if masked_data:
            url = request['path']
            code = http_code
            headers = request['meta']
            body = request['data']
            body = parse_request_body(body)
            log_to_exception(status_type, self.exception_type, code, exception_code, detail, headers, body, url, is_popup,
                         specific_details, request)
            # logger.info(self.exception_type + "|||" + str(code) + "|||" + str(exception_code) + "|||" + str(detail) + "|||" + str(headers) + "|||" + body + "|||" + str(url))
        elif response:
            headers = response.request.headers
            body = response.request.body
            url = response.url
            code = response.status_code
            body = parse_request_body(body)
            log_to_exception(status_type, self.exception_type, code, exception_code, detail, headers, body, url, is_popup,
                         specific_details, request)
            # logger.info(self.exception_type+"|||"+str(code)+"|||"+str(exception_code)+"|||"+str(detail)+"|||"+str(headers)+"|||" + body+"|||"+str(url))
        elif request:
            url = request.path
            code = http_code
            headers = request.META
            if type(request.data) is not dict:
                try:
                    body = request.data.dict()
                except AttributeError:
                    body = ""
            else:
                body = request.data
            body = parse_request_body(body)
            log_to_exception(status_type, self.exception_type, code, exception_code, detail, headers, body, url, is_popup,
                         specific_details, request)
            # logger.info(self.exception_type+"|||"+str(code)+"|||"+str(exception_code)+"|||"+str(detail)+"|||"+str(headers)+"|||" + body+"|||"+str(url))
        else:
            log_to_exception(status_type, self.exception_type, http_code, exception_code, detail, headers, body, url,
                         is_popup, specific_details, request)
            
        self.check_mail_trigger(detail, url, request)

    def check_mail_trigger(self, error_message, url, request):
        """
        if error message is there in one of the keywords then send a mail to the team
        :param self:
        :param error_message: detail of the raise generic exception object
        :return:
        """
        if any(word in error_message for word in api_constants.ERROR_MESSAGE_KEYWORDS):
            self.send_mail(error_message, url, request)

    def send_mail(self, error_message, url, request):
        """
        sending mail for exceptions occured : backend issues
        :return:
        """
        try:
            sys_ip = ""
            try:
                sys_ip = subprocess.check_output("ip a | grep eth | grep inet | awk '{print $2}'", shell=True)
                sys_ip = (str(sys_ip).split('/')[0]).split("'")[1]
            except Exception as e:
                custom_log(level='info', request=request, params={'body': {},
                    'detail': "Error while getting sys_ip for sending mails for exceptions. It was due to" + repr(e)})
            from .email_service import send_email_to_user
            send_email_to_user(
                to_address=settings.SEND_EXCEPTION_NOTIFICATIONS_TO_EMAIL,
                message=pystache.render(api_constants.ERROR_MAIL_MESSAGE, {'error_message': error_message, 'url': url}),
                subject=pystache.render(api_constants.ERROR_MAIL_SUBJECT, {'sys_ip': sys_ip}),
                otp_type="Cron updates",
                request=None
            )
        except Exception as e:
            custom_log(level='info', request=request,
                       params={'body': {}, 'detail': "Error while sending exception mail in exceptions.py due to" + repr(e)})


def error(e):
    if 'detail' in dir(e):
        return e.detail
    else:
        return repr(e)


def get_generic_error_message(headers={}, response_msg='', request=None):
    updated_response_msg = response_msg
    try:
        custom_log(level='info', request=request, params={'body': {'response_msg': response_msg}, 'detail': 'get generic error method called'})
        if request and request is not None:
            if isinstance(request, dict):
                app_os = request.get('meta', {}).get('HTTP_APP_OS', False)
                version_name = request.get('meta', {}).get('HTTP_VERSION_NAME', False)
                version_code = request.get('meta', {}).get('HTTP_VERSION_CODE', False)
            else:
                app_os = request.META.get('HTTP_APP_OS', False)
                version_name = request.META.get('HTTP_VERSION_NAME', False)
                version_code = request.META.get('HTTP_VERSION_CODE', False)
        elif headers and headers is not None:
            app_os = headers.get('HTTP_APP_OS', False)
            version_name = headers.get('HTTP_VERSION_NAME', False)
            version_code = headers.get('HTTP_VERSION_CODE', False)
        else:
            return updated_response_msg
        custom_log(level='info', request=request, params={'body': {"app_os": app_os, "version_name": version_name, "version_code": version_code}, 'detail': 'get generic error method called'})
        if app_os and (version_name or version_code):
            if app_os.lower() in [APP_OS['ANDROID'], APP_OS['IOS']]:
                if app_os.lower() == APP_OS['IOS'] and version_name:
                    digits = version_name.split(".")
                    version_code = int(digits[0]) * 100 + int(digits[1])
                new_configs = AppConfigurations.objects.filter(app_os=app_os.lower(),
                                                               version_code__gt=int(float(version_code)))
            else:
                return updated_response_msg
            if new_configs.count():
                custom_log(level='info', request=request, params={'body': {"app_os": app_os, "version_name": version_name, "version_code": version_code}, 'detail': 'new app config found'})
                if response_msg == api_constants.GENERIC_ERROR_MESSAGE:
                    updated_response_msg = api_constants.GENERIC_ERROR_UPDATE_MESSAGE
                    custom_log(level="info", request=request, params={"body": {"updated_response_msg": updated_response_msg}, "detail": "response msg updated"})
        return updated_response_msg
    except:
        return updated_response_msg

