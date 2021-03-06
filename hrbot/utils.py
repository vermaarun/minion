"""The module contains utility methods"""

from dateparser import parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .models import Employee, LeaveData, EmployeeProfile, Ticket
from .global_variables import EMP_ID, LEAVE_DATE, TICKET_TYPE, \
    TICKET_TO, TICKET_PRIORITY


def apply_leave(statement):
    """
    Checks whether the input statement is a date or not.
    If so, adds date to the global variable.
    """
    input_text = str(statement.text).lower()
    date_obj = parse(input_text, settings={'STRICT_PARSING': True})
    content = {}

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
        result = bool(obj)
    else:
        result = False
    return result


def send_mail(receivers, content):
    """The function is used to send email."""

    sender = 'minion.noreply@gmail.com'
    duration = (content['to_date'] - content['from_date']).days
    duration += 1
    gmail_user = "minion.noreply@gmail.com"
    gmail_pwd = "minionnoreply@123"

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


def createTicket(statement, ticket_data):
    """
    Create Ticket for the user
    :param statement:
    :param ticket_data:
    :return:
    """
    response = ''

    ticket_type = ticket_data.ticket_type
    if ticket_type is None:
        if statement.upper() in TICKET_TYPE:
            ticket_data.ticket_type = statement
        else:
            return "Please select a valid type from the given options or " \
                   "type 'cancel' to exit operation."
        response = """
        Ticket needs to be sent to: 1) IT support, 2) HR support, 
        3) Facility support, 4) App support, 5) Finance support or 'cancel' 
        to exit the operation.
        """
        return response

    ticket_to = ticket_data.ticket_to
    if ticket_to is None:
        if statement.upper() in TICKET_TO:
            ticket_data.ticket_to = statement
        else:
            return "Please select a valid option from the given options or " \
                   "type 'cancel' to exit operation."
        response = "Please provide subject of the Ticket."
        return response

    ticket_subject = ticket_data.ticket_subject
    if ticket_subject is None:
        ticket_data.ticket_subject = statement
        response = "Enter Description of the Ticket"
        return response

    ticket_description = ticket_data.ticket_description
    if ticket_description is None:
        ticket_data.ticket_description = statement
        response = "Please select priority of the Ticket 1) Low, 2) Normal, " \
                   "3) Medium, 4) High, 5) Very High or 'cancel' " \
                   "to exit the operation."
        return response

    ticket_priority = ticket_data.ticket_priority
    if ticket_priority is None:
        if statement.upper() in TICKET_PRIORITY:
            ticket_data.ticket_priority = statement

            response = createTicketWithGivenData(ticket_data)
            ticket_data.clear()
        else:
            return "Please select a valid option from the given options or " \
                   "type 'cancel' to exit operation."
        return response

    if not response:
        response = statement
    return response


def createTicketWithGivenData(ticket_data):
    """
    Create ticket with the entered data by user.
    :param ticket_data:
    :return:
    """
    try:
        ticketDataObj = Ticket(
            emp=Employee.objects.get(emp_id=EMP_ID['emp_id']),
            type=ticket_data.ticket_type,
            to=ticket_data.ticket_to,
            subject=ticket_data.ticket_subject,
            description=ticket_data.ticket_description,
            priority=ticket_data.ticket_priority
        )
        ticketDataObj.save()
        sendMailToUser(ticketDataObj.emp.email_id, ticket_data)
        response = "Ticket created successfully."
    except Exception as e:
        print("***ERROR in creating Ticket", e)
        response = "Something went wrong please try again later."
    return response


def sendMailToUser(receivers, ticket_data):
    """ Method to send email to user after ticket creation. """
    sender = 'minion.noreply@gmail.com'
    mail_user = "minion.noreply@gmail.com"
    mail_pwd = "minionnoreply@123"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Ticket Raised: %s" % ticket_data.ticket_subject
    msg['From'] = sender
    msg['To'] = receivers

    body = """
            <html>
                <body>
                    <p>Dear User,<br/>
                    Your Ticket Request has been 
                    submitted with the following details. <br/><br/>
                    Type: %s <br/>
                    To: %s <br/>
                    Subject: %s <br/>
                    Description: %s <br/>
                    priority: %s<br/><br/>
                    Thanks, <br/>
                    Minion..!!
                    </p>
                </body>
            </html>""" % (ticket_data.ticket_type, ticket_data.ticket_to,
                          ticket_data.ticket_subject,
                          ticket_data.ticket_description,
                          ticket_data.ticket_priority
                          )
    msg.attach(MIMEText(body, 'html'))

    try:
        smtp_obj = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(mail_user, mail_pwd)
        smtp_obj.sendmail(sender, receivers, msg.as_string())
        smtp_obj.close()
        print("Email sent successfully.")
    except Exception as err:
        print("Error: unable to send email: %s " % err)
