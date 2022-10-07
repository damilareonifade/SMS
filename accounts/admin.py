from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (AdminHod, Courses, CustomUser, LeaveReportStaff,
                     LeaveReportStudent, SessionYearModel, Staffs, Student,
                     StudentResult, Subjects)

admin.site.register(CustomUser)
admin.site.register(AdminHod)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Student)
admin.site.register(SessionYearModel)
admin.site.register(StudentResult)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
