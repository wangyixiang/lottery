# -*- coding: utf-8 -*-

from celery.task import task
from lotterywebapp.mail import send_email

@task
def send_email_task(from_, to_, subject, body, html=None, attachments=[]):
    send_email(from_, to_, subject, body, html, attachments)