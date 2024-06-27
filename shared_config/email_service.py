import logging
import smtplib
import os
import requests

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import chain
from . import settings
from django.db.models.query import QuerySet
from .exception_constants import *
from .exceptions import GenericException
from .logging import custom_log
from .models import EmailStatus
from .external_constants import DEFAULT_TIMEOUT

logger = logging.getLogger("default")


def send_email_to_user(to_address, message, subject, otp_type, request, attachment=False, cc_recipient=[], bcc_recipient=[], download_file=True, metadata={}):

    try:
        mail_details = MIMEMultipart('alternative')
        # NOTE: 14917 to specify emails being sent from which server for only QA and UAT
        mail_details['subject'] = "QA" if "10.10.20" in settings.BASE_URL else "UAT" + " | " + subject
        mail_details['from'] = settings.CUSTOM_FROM_EMAIL_ID.get(otp_type, settings.SUPPORT_EMAIL) \
            if 'is_support_mail' in metadata and metadata['is_support_mail'] else settings.SMTP_FROM_EMAIL
        if cc_recipient:
            mail_details['cc'] = ", ".join(cc_recipient)
        if isinstance(to_address, list) or isinstance(to_address, QuerySet):
            temp_to_address = ", ".join(to_address)
            mail_details['to'] = temp_to_address
            cc_recipient = cc_recipient + to_address
            to_address = temp_to_address
        else:
            mail_details['to'] = to_address
            cc_recipient.append(to_address)
        if bcc_recipient:
            mail_details['bcc'] = ", ".join(bcc_recipient)
            # bcc_recipient.append(to_address)
            cc_recipient = list(chain(cc_recipient, bcc_recipient))
        mail_details.add_header('reply-to', settings.REPLY_TO_ADDRESS)
        # Record the MIME type text/html.
        HTML_BODY = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
        mail_details.attach(HTML_BODY)

        file_list = []
        if attachment:
            for files in attachment:
                if 'file' in files:
                    attachFile = MIMEBase('application', 'pdf')
                    attachFile.set_payload(files['file'])
                    encoders.encode_base64(attachFile)
                    attachFile.add_header('Content-Disposition', 'attachment', filename=files.get('file_name', ''))
                    mail_details.attach(attachFile)
                else:
                    path = settings.BASE_DIR + '/' + files.split('/', 3)[-1]
                    file_list.append(download_path(files, path)) if download_file else file_list.append(path)

        for files in file_list:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, 'rb').read())
            encoders.encode_base64(part)
            file_name = files.split('/')[-1]
            part.add_header('Content-Disposition', 'attachment; filename="' + file_name + '"')
            mail_details.attach(part)

        if settings.USE_SMTP_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_DOMAIN, settings.SMTP_PORT)
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        else:
            server = smtplib.SMTP(settings.SMTP_DOMAIN, settings.SMTP_PORT)
        if 'is_support_mail' in metadata and metadata['is_support_mail']:
            from_email = settings.SUPPORT_EMAIL

        elif 'is_investor_mail' in metadata and metadata['is_investor_mail']:
            from_email = settings.INVESTOR_EMAIL

        else:
            from_email = settings.SMTP_FROM_EMAIL

        custom_log(level='info', request=request, params={'body': {"from_email": from_email}, 'detail': 'From email'})
        server.sendmail(from_email, cc_recipient, mail_details.as_string())
        server.quit()
        custom_log(level='info', request=request, params={'body': {"otp_type": otp_type}, 'detail': 'OTP type.'})
        try:
            email = EmailStatus.objects.create(type=otp_type, message_text=message, to_email=to_address,
                                               from_email=from_email)
            custom_log(level='info', request=request,
                       params={'body': {"email_id": str(email.id)}, 'detail': 'Email object created.'})
        except Exception as e:
            raise GenericException(status_type=STATUS_TYPE["EMAIL"], exception_code=RETRYABLE_CODE["EMAIL_FAILURE"],
                                   detail=repr(e), request=request)
        log_data = {
            "detail": "mail_to: " + to_address,
            "body": {
                "message": message,
                "subject": subject
            }
        }
        custom_log("info", request, log_data)
        return {'status': True}
    except GenericException as e:
        raise GenericException(status_type=STATUS_TYPE["EMAIL"], exception_code=RETRYABLE_CODE["EMAIL_FAILURE"],
                               detail=e.detail, request=request)
    except Exception as e:
        body = {
            "to_address": to_address,
            "message": message,
            "subject": subject
        }
        raise GenericException(status_type=STATUS_TYPE["EMAIL"], exception_code=RETRYABLE_CODE["EMAIL_FAILURE"],
                               detail="Email sending error:" + str(e), body=body, request=request)


def download_path(url, path, chunk=2048):
    req = requests.get(url, timeout=DEFAULT_TIMEOUT)
    local_dir = path.rsplit('/', 1)[0] + "/"
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    if req.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in req.iter_content(chunk):
                f.write(chunk)
            f.close()
        return path
    raise Exception('Given url is return status code:{}'.format(req.status_code))
