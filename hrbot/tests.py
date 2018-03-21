"""The module contains all the test cases for the project"""

from datetime import date, datetime
from django.test import TestCase
from .models import Employee, LeaveData, Leave


class HRBotTestCase(TestCase):
    """The class contains test cases for hrbot"""

    def setUp(self):
        self.emp_obj = Employee.objects.create(
            emp_id=13110,
            first_name='akshat',
            last_name='goel',
            designation='development engineer',
            mobile_no=8527484433,
            email_id='akshat.goel@imaginea.com',
            joining_date='2017-12-04',
            creation_time=datetime.now(),
            updated_time=datetime.now()
        )
        self.leave_obj = Leave.objects.create(
            emp_id=13110,
            emp_tbl_id=self.emp_obj,
            first_name='akshat',
            last_name='goel',
            total_leaves=6,
            applied_leaves=0,
            yet_to_accrue=18,
            creation_time=datetime.now(),
            updated_time=datetime.now()
        )
        self.leave_data_obj = LeaveData.objects.create(
            emp_tbl=self.emp_obj,
            first_name='akshat',
            last_name='goel',
            from_date=date(2017, 12, 28),
            to_date=date(2017, 12, 29),
            duration=2,
            valid_days=2,
            creation_time=datetime.now(),
            updated_time=datetime.now()
        )

    # def tearDown(self):
    #     del self.emp_obj
    #     del self.leave_obj
    #     del self.leave_data_obj

    def test_employee(self):
        """Test case for employee model"""

        self.assertTrue(isinstance(self.emp_obj, Employee), 'Employee Object')
        self.assertEqual(self.emp_obj.__str__(), self.emp_obj.first_name)

    def test_leave(self):
        """Test case for leave model"""

        self.assertTrue(isinstance(self.leave_obj, Leave), 'Leave Object')
        self.assertEqual(self.leave_obj.__str__(), self.leave_obj.first_name)

    def test_leave_data(self):
        """Test case for leave data model"""

        self.assertTrue(isinstance(self.leave_data_obj, LeaveData),
                        'Leave Data Object')
        self.assertEqual(self.leave_data_obj.__str__(),
                         self.leave_data_obj.first_name)

# Create your tests here.
