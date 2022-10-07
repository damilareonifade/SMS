import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LeaveNewForm, StudentEditForm, StudentFeedBackForm
from .models import *


@login_required
def dashboard(request):
    return render(request,'students/dashboard.html')

@login_required
def student_edit(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Student.objects.get(id=user)
    if request.method == 'POST':
        form = StudentEditForm(request.POST,instance =student,initial={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'email':user.email,
        })
        if form.is_valid():
            users = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            users.save()
            return redirect('accounts:student_edit')
    else:
        form = StudentEditForm(instace=user)
    return render(request,'accounts/students/edit.html',{'form':form})



@login_required
def student_view_attendance(request):
    student= Student.objects.filter(id=request.user.id)
    course =student.course_id
    subject = Subjects.objects.filter(course=course)
    return render(request,'accounts/student/view_subjects.html',{'subject':subject})

@login_required
def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
 
        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
 
        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
         
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
         
        # Getting Student Data Based on Logged in Data
        stud_obj = Student.objects.get(admin=user_obj)
 
        # Now Accessing Attendance Data based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
                                                                       end_date_parse),
                                               subject_id=subject_obj)
        # Getting Attendance Report based on the attendance
        # details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                             student_id=stud_obj)
 
         
        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }
 
        return render(request, 'student_template/student_attendance_data.html', context) 

@login_required
def student_leave(request):
    student = CustomUser.objects.filter(id=request.user.id)
    leave_report= LeaveReportStudent.objects.filter(student_id=student)

    return render(request,'accounts/student/all_leave.html',{'leave_report':leave_report})

@login_required
def student_new_leave(request):
    student= CustomUser.objects.filter(id=request.user.id)
    if request.method == 'POST':
        form = LeaveNewForm(request.POST)
        if form.is_valid():
            leave_form = form.save(commit=False)
            leave_form.student_id = student
            leave_form.save()
            messages.success(request,'You have successfully requested for a new leave')
            return render('accounts:student_leave')
    else:
        form = LeaveNewForm()
    return render(request,'accounts/student/new_leave.html',{'form':form})

@login_required
def student_feedback(request):
    student = Student.objects.filter(admin=request.user.id)
    feedback = FeedBackStudent(student_id=student)
    return render(request,'accounts/student/student_feedback_list.html',{'feedback':feedback})

@login_required
def student_feedback_create(request):
    student = Student.objects.filter(admin=request.user.id)
    if request.method == 'POST':
        form = StudentFeedBackForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.student_id=student.id
            user.feedback_reply = ""
            user.save()
            messages.success(request,'You have submitted a feedback to the school authorities')
            return redirect('accounts:student_feedback')

    else:
        form = StudentFeedBackForm()
    return render(request,'accounts/student/feedback_form.html',{'form':form})



