"""The module contains utility methods"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from datetime import datetime
from dateparser import parse
from .models import Employee, LeaveData, EmployeeProfile
from .global_variables import EMP_ID
from .global_variables import LEAVE_DATE


def apply_leave(statement):
    """Checks whether the input statement is a date or not.
    If so, adds date to the global variable.
    """
    input_text = str(statement.text).lower()
    date_obj = parse(input_text, settings={'STRICT_PARSING': True})
    content = {}
    # print(date_obj)
    # print(LEAVE_DATE)

    if date_obj:
        if 'from_date' not in LEAVE_DATE:
            LEAVE_DATE['from_date'] = date_obj.date()
            response = "Please enter 'To' date."
        else:
            LEAVE_DATE['to_date'] = date_obj.date()
            emp_data = Employee.objects.get(emp_id=EMP_ID['emp_id'])
            duration = (LEAVE_DATE['to_date'] - LEAVE_DATE['from_date']).days
            duration += 1

            leave_data = LeaveData(emp_tbl=emp_data)
            leave_data.first_name = emp_data.first_name
            leave_data.last_name = emp_data.last_name
            leave_data.from_date = LEAVE_DATE['from_date']
            leave_data.to_date = LEAVE_DATE['to_date']
            leave_data.duration = duration
            leave_data.valid_days = duration

            leave_data.save()
            response = "Your leave has been applied successfully."

            # Send email to the user.
            content['from_date'] = LEAVE_DATE['from_date']
            content['to_date'] = LEAVE_DATE['to_date']
            content['full_name'] = '%s %s' % (emp_data.first_name,
                                              emp_data.last_name)

            send_mail([emp_data.email_id], content)
            del LEAVE_DATE['from_date']
            del LEAVE_DATE['to_date']

        return response
    else:
        return None


def validate_id(text):
    """The function checks if the string is a valid employee id"""

    if text.isdigit():
        obj = EmployeeProfile.objects.get(emp_id=int(text))
        # if obj:
        #     result = True
        # else:
        #     result = False
        result = bool(obj)
    else:
        result = False

    return result


def send_mail(receivers, content):
    """The function is used to send email."""

    sender = 'akshat.goel@imaginea.com'
    duration = (content['to_date'] - content['from_date']).days
    duration += 1
    # receivers = to
    gmail_user = "akshat.goel@imaginea.com"
    gmail_pwd = ""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Leave Application: From %s To %s %s " \
                     "day(s) leave Applied" \
                     % (content['from_date'].strftime('%d-%b-%Y'),
                        content['to_date'].strftime('%d-%b-%Y'),
                        str(duration))
    msg['From'] = sender
    msg['To'] = receivers[0]

    body = """
        <html>
            <body>
                <p>Dear %s,<br/>
                Your Leave Application Request has been 
                submitted with the following details. <br/><br/>
                Leave Application:<br/>
                Type: Paid Time Off (PTO)<br/>
                From: %s <br/>
                To: %s <br/>
                Total Days: %s <br/>
                Reason: <br/><br/>
                Thanks, <br/>
                HR Bot
                </p>
            </body>
        </html>""" % (content['full_name'].title(),
                      content['from_date'].strftime('%d-%b-%Y'),
                      content['to_date'].strftime('%d-%b-%Y'),
                      str(duration))
    msg.attach(MIMEText(body, 'html'))

    try:
        smtp_obj = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(gmail_user, gmail_pwd)
        smtp_obj.sendmail(sender, receivers, msg.as_string())
        smtp_obj.close()
        print("Email sent successfully.")
    except Exception as err:
        print("Error: unable to send email: %s " % err)
