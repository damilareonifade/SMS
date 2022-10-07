from django.contrib import admin

from finance.models import Courses, Finance, Role, Student

admin.site.register(Finance)
admin.site.register(Courses)
admin.site.register(Student)
admin.site.register(Role)