#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for reporting student results in several different
formats.
"""
import smtplib
import email
import datetime

def send(report, report_text, student=None):
    """
    Main method that sends off the report
    """
    SENDERS = {
        "email": send_email,
        "file": send_file
    }

    send_method = report["send_method"]
    SENDERS[send_method](report, report_text, student)

def send_email(report, report_text, student):
    """
    Send the text over the email
    """
    message = email.message_from_string(report_text)
    message['To'] = transform_format_codes(report['destination'], student)
    message['From'] = transform_format_codes(report['source'], student)
    message['Subject'] = transform_format_codes(report['subject'], student)
    #TODO support greater variety of smtp servers types as well as smtps
    with smtplib.SMTP('localhost') as email_server:
        email_server.send_message(message)

def send_file(report, report_text, student):
    """
    Send the text to a file
    """
    destination = transform_format_codes(report['destination'], student)
    with open(destination, 'w') as outfile:
        outfile.write(report_text)


def transform_format_codes(dest, student):
    """
    transform the destination address to use format codes
    """
    if student is None and ("%u" in dest or "%e" in dest):
        raise Exception
    elif student is not None:
        dest = dest.replace('%u', student['username'])
        dest = dest.replace('%e', student['email'])
    date = str(datetime.date.today())
    dest = dest.replace('%d', date)
    return dest

