"""This module contains DynamicAdaptor that processes input
statement and fetches information from the database.
"""
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from django.db.models import Q
from chatterbot.conversation import Statement
from ..models import Employee, Leave
from ..global_variables import EMP_ID, OTHER_EMP_ID
from ..utils import apply_leave, validate_id


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
            ]
        }

        # Field names, keyword mapping
        self.db_keyword_map = {
            # 'employee id': 'emp_id',
            # 'employee code': 'emp_id',
            # 'designation': 'designation',
            # 'first name': 'first_name',
            # 'last name': 'last_name',
            # 'email': 'email_id',
            # 'email id': 'email_id',
            # 'emailid': 'email_id',
            'total leaves': 'total_leaves',
            'applied leaves': 'applied_leaves',
            'mobile number': 'mobile_no',
            # 'joining date': 'joining_date',
            # 'date of joining': 'joining_date',
            'remaining leaves': 'remaining leaves',
            'yet accrue': 'yet_to_accrue'
        }

    def can_process(self, statement):
        """Checks whether the statement can be processed or not."""

        print('______Inside Can Process______')
        # input_text = str(statement.text).lower()
        #
        # if parse(input_text):
        #     return True
        # elif validate_text(input_text.split(), self.module_keywords):
        #     return True
        # else:
        #     return False
        return True

    def process(self, statement):
        """Processes the input statement and respond back with
        appropriate response.
        """

        print('______Inside Process______')
        input_text = str(statement.text).lower().rstrip('?.')
        text_list = input_text.split()
        response = Statement(text=input_text)
        reset_response = "If you wish to know details about another " \
                         "employee or you wish to switch to your own " \
                         "employee id, please type the employee id. " \
                         "Please ignore in case you are using your id."
        emp_id = EMP_ID['emp_id']

        # if 'emp_id' in OTHER_EMP_ID:
        #     emp_id = OTHER_EMP_ID['emp_id']

        # if validate_id(input_text):
        #     value = int(input_text)
            # if value == EMP_ID['emp_id']:
            #     if 'emp_id' in OTHER_EMP_ID:
            #         del OTHER_EMP_ID['emp_id']
            #
            #     response.text = "Employee id switched. Please tell me what" \
            #                     " you wish to know."
            #     response.confidence = 1
            # else:
            #     emp_id = OTHER_EMP_ID['emp_id'] = value
            #     response.text = "Employee id switched. Please tell me what" \
            #                     " you wish to know."
            #     response.confidence = 1

        # else:
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
                # field = self.db_keyword_map[text_keyword]
                if key == 'Employee':
                    # data = list(Employee.objects.filter(
                    #     emp_id=emp_id).values())
                    response.text = "I am sorry I don't understand. " \
                                    "Please enter the name to know details."
                    # response.text += str(data[0][field]).title()
                    # response.text += ".<br> %s" % reset_response
                    response.confidence = 1
                #
                # elif key == 'Leave' and 'emp_id' in OTHER_EMP_ID:
                #     response.text = 'Sorry! Leave data of other ' \
                #                     'employees is confidential. %s' % \
                #                     reset_response
                #     response.confidence = 1

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
            qset = Q(full_name__icontains="".join(text_list))
            emp_obj = list(Employee.objects.filter(qset).values())
            if emp_obj:
                if len(emp_obj) > 1:
                    result = "Please find the matching results below:<br>"
                    for emp in emp_obj:
                        result += "Name: %s %s <br>" %(
                            emp['first_name'].title(),
                            emp['last_name'].title())
                    result += "Enter the name to know details."
                else:
                    result = "Please find the details below:<br>"
                    for emp in emp_obj:
                        # print(emp)
                        result += "Name: %s %s <br>Designation: %s<br>" \
                                  "Employee Id: %s<br>" \
                                  "Mobile No.: %s<br>Email Id: %s" %(
                            emp['first_name'].title(),
                            emp['last_name'].title(),
                            emp['designation'].title(),
                            emp['emp_id'], emp['mobile_no'],
                            emp['email_id'])
            else:
                result = apply_leave(statement)
            if result:
                response.text = result
                response.confidence = 1
            else:
                response.text = "I am sorry! I don't understand. " \
                                "Please try out some other keywords."
                response.confidence = 0.9
        print(response.text)
        return response
