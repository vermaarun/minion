"""This module contains DynamicAdaptor that processes input
statement and fetches information from the database.
"""
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from django.db.models import Q
from chatterbot.conversation import Statement
from ..models import Employee, Leave
from ..global_variables import EMP_ID
from ..utils import apply_leave

SEARCH_FLAG = False


class DynamicAdaptor(LogicAdapter):
    """The DynamicAdaptor logic adaptor parses input to
    extract the keywords related to employee's information.
    If keyword found, the corresponding information returned
    as result.
    """

    def __init__(self, **kwargs):
        super(DynamicAdaptor, self).__init__(**kwargs)

        # Keywords that user can input
        self.module_keywords = {
            'Employee': [
                'employee id', 'employee code', 'designation', 'name',
                'email', 'mobile', 'email id', 'emailid', "number"
            ],
            'Leave': [
                'total leaves', 'applied leaves', 'remaining leaves',
                'yet accrue'
            ],
            'search': [
                'find employee', 'search employee', 'employee details',
                'employee detail', 'employee information', 'employee info'
            ]
        }

        # Field names, keyword mapping
        self.db_keyword_map = {
            'total leaves': 'total_leaves',
            'applied leaves': 'applied_leaves',
            'mobile number': 'mobile_no',
            'remaining leaves': 'remaining leaves',
            'yet accrue': 'yet_to_accrue'
        }

    def can_process(self, statement):
        """Checks whether the statement can be processed or not."""

        print('______Inside Can Process______')
        return True

    def process(self, statement):
        """Processes the input statement and respond back with
        appropriate response.
        """

        print('______Inside Process______')
        global SEARCH_FLAG
        input_text = str(statement.text).lower().rstrip('?.')
        text_list = input_text.split()
        response = Statement(text=input_text)
        reset_response = "If you wish to know details about another " \
                         "employee or you wish to switch to your own " \
                         "employee id, please type the employee id. " \
                         "Please ignore in case you are using your id."

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

            if status:
                if key == 'Employee':

                    response.text = "I am sorry I don't understand. " \
                                    "Please enter the name to know details."
                    response.confidence = 1
                elif key == 'search':
                    SEARCH_FLAG = True
                    response.text = "Please enter employee name"
                    response.confidence = 1

                elif key == 'Leave':
                    data = list(
                        Leave.objects.filter(
                            emp_id=EMP_ID['emp_id']
                        ).values()
                    )
                    response.text = text_keyword.title() + ': '
                    if text_keyword.replace(' ', '_') == 'remaining_leaves':
                        rem_leaves = (
                            int(data[0]['total_leaves'])
                            - int(data[0]['applied_leaves'])
                        )
                        response.text += str(rem_leaves)
                    else:
                        response.text += str(data[0][field])
                    response.confidence = 1
                break

        if response.confidence == 0:
            if SEARCH_FLAG:
                qset = Q(full_name__icontains=text_list[0])
                emp_obj = list(Employee.objects.filter(qset).values())
                if emp_obj:
                    result = "Please find the matching results below:<br>"
                    for emp in emp_obj:
                        if "".join(text_list).lower() == \
                                emp['full_name'].replace(' ','').lower():
                            result = "Please find the details below:<br>"
                            result += "Name: %s<br>Designation: %s<br>" \
                                      "Employee Id: %s<br>" \
                                      "Mobile No.: %s<br>Email Id: %s" % (
                                emp['full_name'].title(),
                                emp['designation'].title(),
                                emp['emp_id'], emp['mobile_no'],
                                emp['email_id'])
                            SEARCH_FLAG = False
                            break
                        else:
                            result += "Name: %s<br>" % (
                                emp['full_name'].title())

                else:
                    result = "I am sorry! I am not able to find the employee" \
                             " you are looking for"
                    SEARCH_FLAG = False
            else:
                result = apply_leave(statement)
            if result:
                response.text = result
                response.confidence = 1
            else:
                response.text = "I am sorry! I don't understand. " \
                                "Please refer FAQs from sidebar."
                response.confidence = 0.9
        return response
