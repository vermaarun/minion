"""
This module contains TicketAdaptor that processes input
statement and raise the ticket on behalf of user.
"""
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

from ..global_variables import EMP_ID, OTHER_EMP_ID
from ..utils import createTicket

ticket_flag = False


class TicketAdaptor(LogicAdapter):
    """The TicketAdaptor logic adaptor parses input to
    extract the keywords related to employee's information.
    If keyword found, the corresponding information returned
    as result.
    """

    def __init__(self, **kwargs):
        super(TicketAdaptor, self).__init__(**kwargs)

        # Keywords that user can input
        self.module_keywords = {
            'Ticket': [
                'ticket', 'create a ticket', 'raise ticket',
                'issue'
            ]
        }

    def can_process(self, statement):
        """Checks whether the statement can be processed or not."""
        return True

    def process(self, statement):
        """Processes the input statement and respond back with
        appropriate response.
        """
        global ticket_flag
        result = ''
        input_text = str(statement.text).lower().rstrip('?.')
        text_list = input_text.split()
        response = Statement(text=input_text)
        reset_response = "If you wish to know details about another " \
                         "employee or you wish to switch to your own " \
                         "employee id, please type the employee id. " \
                         "Please ignore in case you are using your id."
        emp_id = EMP_ID.get('emp_id', None)

        for key, val in self.module_keywords.items():
            status = []
            text_keyword = None

            for word in val:
                word_list = word.split()
                status = [
                    True if x in text_list else False
                    for x in word_list
                ]
                if False not in status:
                    text_keyword = word
                    break
                else:
                    status = []

            if status and not ticket_flag:
                response.confidence = 1
                result = "Please select type of ticket you want to create " \
                         "1) Default 2) Incident 3) Problem 4) Request for" \
                         " Change"
                ticket_flag = True
            else:
                if ticket_flag:
                    result = createTicket(statement.text)
                    response.confidence = 1
                    if result == "Ticket created successfully.":
                        ticket_flag = False
                else:
                    response.confidence = 0

        if result:
            response.text = result
        else:
            response.text = "I'm sorry! I don't understand. " \
                            "Please try out some other keywords."
            response.confidence = 0.9
        return response
