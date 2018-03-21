"""The module contains Middleware that processes request and
set variables.
"""

from .models import Employee
from .global_variables import EMP_ID


class Middleware(object):
    """The Middleware processes the http request and sets
    relevant user information in variables.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Processes the http request and sets necessary variables
        in global_variables module.
        """

        data = list(Employee.objects.filter(email_id=request.user).values())
        if data:
            EMP_ID['emp_id'] = data[0]['emp_id']
            print('======== %s' % EMP_ID['emp_id'])

        response = self.get_response(request)
        return response

    # def process_request(self, request):
    #     """Undefined public method."""
    #
    #     pass
