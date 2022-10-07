from django.contrib.auth.views import LoginView
from django.urls import path

from . import adminview, staffview, studentview, views

app_name = 'accounts'

urlpatterns = [
    path('login/',LoginView.as_view(template_name='accounts/register.html/login'),name='login'),
    path('register/',views.register,name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate,name='activate'),

    #Students URLS
    path('dashboard/',studentview.dashboard,name='students_home'),
    path('student/edit-profile/',studentview.student_edit,name='student_edit'),
    path('student/view-attendance/',studentview.student_view_attendance,name='student_view_attendance'),
    path('student/leave/',studentview.student_leave,name='student_leave'),
    path('student/new_leave',studentview.student_new_leave,name='student_new_leave'),
    path('student/feedback_list/',studentview.student_feedback,name='student_feedback'),
    path('student/feedback_create/',studentview.student_feedback_create,name='student_feedback_create'),


    #Staff urls
    path('dashboard/',staffview.staff_home,name='dashboard'),
    path('staff/profile/',staffview.staff_profile,name='staff_profile'),
    path('staff/update/',staffview.staff_update,name='staff_update'),
    path('staff/apply-leave/',staffview.staff_apply_leave,name='staff_leave'),
    path('staff/role/',staffview.staff_subject,name='staff_subject'),


    #Admin Url
    path('dashboard',adminview.admin_home,name='admin_home'),
    path('add/staffs/',adminview.add_staff,name='add_staff'),
    path('admin/all_staff/',adminview.view_staff,name='all_staff'),
    path('admin/edit_staff/<slug:staff_id>/',adminview.edit_staff,name='edit_staff'),
    path('admin/delete_staff/<slug:staff_id>/',adminview.delete_staff,name='delete_staff'),
    path('admin/add-course/',adminview.add_course,name='add_course'),
    path('admin/all-courses/',adminview.all_courses,name='all_courses'),
    path('admin/edit-course/<slug:course_id>/',adminview.edit_course,name='edit_course'),
    path('admin/delete_course/<slug:course_id>/',adminview.delete_course,name='delete_course'),
    path('admin/all-sessions/',adminview.all_sessions,name='all_sessions'),
    path('admin/create-sessions/',adminview.add_session,name='add_sessions'),
    path('admin/edit-sessions/<slug:session_id>/',adminview.edit_session,name='edit_sessions'),
    path('admin/delete-sessions/<slug:session_id>/',adminview.delete_session,name='delete_session'),
    path('admin/all-students/',adminview.all_students,name='all_students'),
    path('admin/add-students/',adminview.add_students,name='add_student'),
    path('admin/filter-students/',adminview.filtered_students,name='filtered_students'),
    path('admin/edit-students/<int:student_id>/',adminview.edit_student,name='edit_student'),
    path('admin/delete-students/<slug:student_id>/',adminview.delete_student,name='delete_student'),
    path('admin/all-subject/',adminview.all_subjects,name='all_subjects'),
    path('admin/create-subject',adminview.add_subject,name='add_subject'),
    path('admin/edit-subject/<slug:subject_id>',adminview.edit_subject,name='edit_subject'),
    path('admin/delete-subject/<slug:subject_id>/',adminview.delete_subject,name='delete_subject'),

]
