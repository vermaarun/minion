"""The module is used to plug in custom model
with django admin.
"""

from django.contrib import admin
from .models import Employee, Leave, EmployeeProfile, Ticket


class EmployeeAdmin(admin.ModelAdmin):
    """The EmployeeAdmin plugs in Employee model with admin panel."""

    list_display = (
        'emp_id',
        'first_name',
        'last_name',
        'designation',
        'mobile_no',
        'email_id',
        'joining_date',
    )
    list_filter = ('emp_id', )
    # search_fields = ('text', )


class LeaveAdmin(admin.ModelAdmin):
    """The LeaveAdmin plugs in Leave model with admin panel."""

    list_display = (
        'emp_id',
        'first_name',
        'last_name',
        'total_leaves',
        'applied_leaves',
        'yet_to_accrue',
    )
    # search_fields = ['emp_id', ]
class EmployeeProfileAdmin(admin.ModelAdmin):
    """The EmployeeAdmin plugs in Employee model with admin panel."""

    list_display = (
        'emp_id',
        'first_name',
        'last_name',
        'designation',
        'mobile_no',
        'email_id',
        'joining_date',
    )
    list_filter = ('emp_id', )

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(Ticket)
