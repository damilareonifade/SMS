import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import EditStaffForm, StudentReportForm
from .models import (Attendance, AttendanceReport, Courses, CustomUser,
                     LeaveReportStaff, SessionYearModel, Staffs, Student,
                     StudentResult, Subjects)


@login_required
def staff_home(request):
    return render(request,'accounts/admin/home.html')


@login_required
def staff_create_attendance(request):
    subject = Subjects.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.objects.all()
    return render(request,'accounts/staff/take_attendance.html',{'subject':subject,'session_year':session_year})


@login_required
def staff_apply_leave(request):
    user = request.user.id
    if request.method == 'POST':
        form = LeaveReportStaff(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.staff_id = user
            user.save()
            messages.success(request,'Your leave have been applied')
            return redirect('accounts:staff_home')
    else:
        form = LeaveReportStaff()
    return render(request,'acscounts/staff/staff_leave.html',{'form':form})

#subjects taught by staff
@login_required
def staff_subject(request):
    staff = request.user.id
    subject = Subjects.objects.filter(staff=staff)
    return render(request,'accounts/staff/subjects.html',{'subject':subject})


#view to give all the student offering a particular course
@login_required
def get_students(request):
    subject_id = request.POST.get('subject')
    session_year = request.POST.get('session_year_id')

    subjects = Subjects.objects.get(id=subject_id)
    sessionyear = SessionYearModel.objects.get(id=session_year)

    student = Student.objects.filter(course_id = subjects.course.id,session_year=sessionyear)
    list_data = []
    for student in student:
        data_small = {'id':student.admin.id,'name':student.admin.first_name}
        list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data),content_type="application/json", safe=False)

@login_required
def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff= Staffs.objects.filter(id=user)
    return render(request,'accounts/staff/profile.html',{'user':user,'staff':staff})

@login_required
def staff_update(request,staff_id):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user.id)
    if request.method == 'POST':
        form = EditStaffForm(request.POST,instance=staff,initial={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'username':user.username
        })
        if form.is_valid():
            user= form.save(commit=False)
            user.first_name=form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username=form.cleaned_data['username']
            staff.address = form.cleaned_data['address']
            user.save()
            staff.save()
            messages.success(request,'Your profile has been updated')
            return redirect('accounts:dashboard')
    else:
        form = EditStaffForm()
    return render(request,'accounts/staff/update.html',{'form':form})

def staff_result(request):
    subject = Subjects.objects.filter(staff = request.user.id)
    sessionyear = SessionYearModel.objects.all()
    return render(request,'accounts/staff/staff_result.html',{'subject':subject,'sessionyear':sessionyear })


@login_required
def staff_update_result(request,student_admin_id,subject_id):
    student_id = Student.objects.get(admin = student_admin_id)
    subject_id = Subjects.objects.get(id = subject_id)
    student = StudentResult.objects.get(student_id=student_id,subject_id=subject_id).exists()
    if student is True:
        if request.method == 'POST':
            form = StudentReportForm(request.POST, instance = student)
            if form.is_valid():
                user = form.save(commit=False)
                user.student_id = student_id
                user.subject_id = subject_id
                user.save()
                messages.success(request,'Your form has been saved successfully')
                return redirect('accounts:staff_result')
        else:
            form = StudentReportForm()
    
    else:
        if request.method == 'POST':
            form = StudentReportForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.subject.id = student_id
                user.subject_id = subject_id
                user.save()
                messages.success(request,'Student Score has been added')
                return redirect('accounts:staff_result')
        else:
            form = StudentReportForm()
    return render(request,'accounts/staff/add_scores.html',{'form':form})
