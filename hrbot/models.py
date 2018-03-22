"""The module is used to define models."""

from datetime import datetime
from django.db import models


class Employee(models.Model):
    """The Employee model creates the table with
    relevant fields defined in database.
    """

    emp_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=200, default='', blank=True)
    last_name = models.CharField(max_length=200, default='', blank=True)
    full_name = models.CharField(max_length=200, default='', blank=True)
    designation = models.CharField(max_length=200, default='', blank=True)
    mobile_no = models.IntegerField(default=0)
    email_id = models.EmailField(default='', blank=False)
    joining_date = models.DateField()
    creation_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.now()
        if not self.updated_time:
            self.updated_time = datetime.now()
        super(Employee, self).save(*args, **kwargs)


class Leave(models.Model):
    """The Leave model creates the table with
    relevant fields defined in database.
    """

    emp_id = models.IntegerField(unique=True, primary_key=True)
    emp_tbl_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    total_leaves = models.IntegerField(default=6)
    applied_leaves = models.DecimalField(default=0.0, decimal_places=1,
                                         max_digits=5)
    yet_to_accrue = models.IntegerField(default=18)
    creation_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.now()
        if not self.updated_time:
            self.updated_time = datetime.now()
        super(Leave, self).save(*args, **kwargs)


class LeaveData(models.Model):
    """The LeaveData models creates a table with
    employee's leave data.
    """

    emp_tbl = models.ForeignKey(Employee, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    from_date = models.DateField()
    to_date = models.DateField()
    leave_type = models.CharField(default='paid time off', max_length=100)
    duration = models.IntegerField(default=0)
    # duration = models.DecimalField(default=0.0, max_digits=3,
    #                                decimal_places=1)
    # valid_days = models.DecimalField(default=0.0, decimal_places=1,
    #                                  max_digits=3)
    leave_status = models.CharField(default='pending', max_length=100)
    creation_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.now()
        if not self.updated_time:
            self.updated_time = datetime.now()
        super(LeaveData, self).save(*args, **kwargs)


class EmployeeProfile(models.Model):
    """The EmployeeProfile model creates fields related to
    employee profile.
    """

    emp_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=200, default='', blank=True)
    last_name = models.CharField(max_length=200, default='', blank=True)
    designation = models.CharField(max_length=200, default='', blank=True)
    mobile_no = models.IntegerField(default=0)
    email_id = models.EmailField(default='', blank=False)
    joining_date = models.DateField()
    creation_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.now()
        if not self.updated_time:
            self.updated_time = datetime.now()
        super(EmployeeProfile, self).save(*args, **kwargs)


class Ticket(models.Model):
    """ Ticket model to create object for every ticket raised by employees. """

    type_choice = (
        ('DEFAULT', 'Default'),
        ('INCIDENT', 'Incident'),
        ('PROBLEM', 'Problem'),
        ('Request for Change', 'Request For Change')
    )
    to_choice = (
        ('IT', 'IT support'),
        ('HR', 'HR support'),
        ('FACILITY', 'Facility support'),
        ('APP', 'App support'),
        ('FINANCE', 'Finance support')
    )
    priority_choice = (
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('VERY HIGH', 'Very High')
    )

    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=10, choices=type_choice)
    to = models.CharField(max_length=10, choices=to_choice)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    priority = models.CharField(max_length=10, choices=priority_choice)

    def __str__(self):
        """ Method to print Ticket object. """
        return self.subject

