from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import (AddminForm, AddStaffForm, AddStudentForm, AddSubjectForm,
                    CreateCourseForm, EditCourseForm, EditStaffForm,
                    EditSubjectForm, SessionYearEditForm, SessionYearForm,
                    StudentEditForm)
from .models import *


def admin_home(request):
     
    all_student_count = Student.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
 
    for course in course_all:
        # No of subjects in the course
        subjects = Subjects.objects.filter(course=course.id).count()
        # number of students offering the course
        students = Student.objects.filter(course_id=course.id).count()
        course_name_list.append(course.courses)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)
     
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course.id)
        student_count = Student.objects.filter(course_id=course.id).count()
        #Understood to this point
        subject_list.append(subject.subject)
        student_count_list_in_subject.append(student_count)
     
    # For Saffs
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]
 
    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id,
                                                 leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)
 
    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]
    students = Student.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id,
                                                     status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id,
                                                 status=False).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)
 
 
    context={
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
        }
    return render(request,'accounts/admin/home.html',context)

@transaction.atomic()
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            custom = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,role='STUDENT')
            user.admin=custom
            user.save()
            current_site = get_current_site(request)
            subject = "Activate Your Account"
            message = render_to_string('accounts/registrations/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject=subject, message= message)
            messages.success(request, "Student Added Successfully!")
            return redirect('accounts:add_student')
    
    else:
        form = AddStudentForm()
    
    return render(request,'accounts/admin/add_student.html',{'form':form})

@transaction.atomic()
def add_staff(request):
    if request.method == 'POST':
        form = AddStaffForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            custom = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=password,role='TEACHER')
            user.admin = custom
            user.save()
            # current_site = get_current_site(request)
            # subject = "Activate Your Account"
            # message = render_to_string('accounts/registrations/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # send_mail(subject='A cool subject',message='A stunning message',from_email=settings.EMAIL_HOST_USER,recipient_list=['damilareonifade34@gmail.com'])
            messages.success(request, "Staff Added Successfully!")
            return redirect('accounts:all_staff')
    
    else:
        form = AddStaffForm()
    
    return render(request,'accounts/admin/add_staff.html',{'form':form})


def view_staff(request):
    user = CustomUser.objects.filter(is_active=True)
    staff = Staffs.objects.filter(admin__in=user)
    return render(request,'accounts/admin/all_staff.html',{'staff':staff})


@transaction.atomic()
def edit_staff(request,staff_id):
    user = Student.objects.get(id=staff_id)
    if request.method == 'POST':
        form = EditStaffForm(request.POST or None,request.FILES, instance=user, initial = {'address': user.address,})
        if form.is_valid():
            user = form.save(commit=False)
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = form.cleaned_data['address']
            staff_model.save()
            messages.success(request, "Staff Updated Successfully.")
            return redirect('account:all_staff')
    else:
        form = EditStaffForm()
    return render(request,'account/admin/edit_staff.html',{'form':form})

@transaction.atomic()
def delete_staff(request,staff_id):
    staff = Staffs.objects.get(id=staff.id)
    try:
        staff.admin.is_active = False
        staff.admin.save()
        messages.succes(request,'Staff has been deleted')
        return redirect('accounts:all_staff')
    except:
        messages.error(request,'Error occured while deleting staff')
        return redirect('accounts:all_staff')


@transaction.atomic()
def add_course(request):
    if request.method == 'POST':
        try:
            form = CreateCourseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Course has been added successfully')
                return redirect('accounts:all_courses')
        except:
            form = CreateCourseForm()
            messages.error(request,'TFailed to register course')
    else:
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    return render(request,'accounts/admin/add_course.html',{'form':form})


def all_courses(request):
    course = Courses.objects.all()
    return render(request,'accounts/admin/all_courses.html',{'course':course})


@transaction.atomic()
def edit_course(request,course_id):
    course = Courses.objects.get(id=course_id)
    print(course)
    if request.method == 'POST':
        try:
            form = EditCourseForm(request.POST,instance=course)
            if form.is_valid():
                form.save()
                messages.success(request,'Your Course name has been updated')
                return render('account:all_courses')
        except:
            form = EditCourseForm(request.POST,instace=course)
            messages.error(request,'There is an error in submiting your form')
    
    else:
        form = EditCourseForm()
    return render(request,'accounts/admin/edit_course.html',{'form':form})


@transaction.atomic()
def delete_course(request,course_id):
    print(course_id)
    course = Courses.objects.get(id = course_id)
    course.delete()

    # try:        
    #     course.delete()
    #     messages.success(request,'The specified course has been deleted')
    #     return redirect('accounts:all_courses')
    # except:
    #     messages.error(request,'Your request cannot be processed at the moment')
    #     return redirect('accounts:all_courses')

def all_sessions(request):
    session = SessionYearModel.objects.all()
    return render(request,'accounts/admin/all_sessions.html',{'session':session})


def add_session(request):
    if request.method == 'POST':
        form = SessionYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your form has been saved')
            return redirect('accounts:all_sessions')
    else:
        form = SessionYearForm()
    return render(request,'accounts/admin/add_session.html',{'form':form})


def edit_session(request,session_id):
    sessions = SessionYearModel.objects.get(id=session_id)
    if request.method == 'POST':
        form = SessionYearEditForm(request.POST,instance=sessions)
        if form.is_valid():
            form.save()
            messages.success(request,'Sessions has been updated ')
            return redirect('accounts:all_sessions')
    else:
        form = SessionYearEditForm()
    return render(request,'accounts/admin/edit_session.html',{'form':form})

def delete_session(request,session_id):
    sessions = SessionYearModel.objects.filter(id=session_id)
    try:
        sessions.delete()
        messages.success(request,'Your form has ben deleted')
        return redirect('accounts:all_sessions')
    except:
        messages.success(request,'Something went wrong try again later')
        return redirect('accounts:all_sessions')


def add_students(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_password = password + '123'
            custom = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name,email=email,password=user_password,role='STUDENTS')
            user.admin = custom
            # current_site = get_current_site(request)
            # subject = "Activate Your Account"
            # message = render_to_string('accounts/registrations/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # user.email_user(subject=subject, message= message)
            messages.success(request, "Staff Added Successfully!")
            return redirect('accounts:all_students')
    else:
        form = AddStudentForm()
    return render(request,'accounts/admin/add_student.html',{'form':form})



def edit_student(request,student_id):
    student = Student.objects.get(id=student_id)
    if request.method == "POST":
        form = StudentEditForm(request.POST,instance=student,initial = {'first_name':student.admin.first_name,
            'last_name':student.admin.last_name,
            'username':student.admin.username,
            'email':student.admin.email})        
        if form.is_valid():
            user = form.save(commit=False)
            user.admin.first_name = form.cleaned_data['first_name']
            user.admin.last_name = form.cleaned_data['last_name']
            user.admin.username = form.cleaned_data['username']
            user.admin.email = form.cleaned_data['email']
            user.save()
            messages.success(request,'Student account activated')
            return redirect('accounts:all_students')
    else:
        form = StudentEditForm()
    return render(request,'accounts/admin/edit_students.html',{'form':form})

def delete_student(request,student_id):
    student = Student.objects.get(id= student_id)
    try:
        student.admin.is_active=False
        student.admin.save()
        messages.success(request,'Student is not active')
        return redirect('accounts:all_students') 
    except:
        messages.error(request,'There is an error from the server side')
        return redirect('accounts:all_students')

def all_students(request):
    user = CustomUser.objects.filter(is_active=True)
    student = Student.objects.filter(admin__in=user)
    return render(request,'accounts/admin/all_students.html',{'student':student})

def filtered_students(request):
    student_level = request.POST.get('student_level')
    student_name = request.POST.get('student_name')

    user = CustomUser.objects.filter(is_active=True)
    student = Student.objects.filter(admin__in=user,level=student_level)
    
    return render(request,'accounts/')
    

def add_subject(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Subject has been added successfully')
            return redirect('accounts:all_subjects')
    else:
        form = AddSubjectForm()
    return render(request,'accounts/admin/add_subject.html',{'form':form})

def edit_subject(request,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    print(subject)
    if request.method == "POST":
        form = EditSubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request,'Subject edited succesfully')
            return redirect('accounts:all_subjects')
    else:
        form = EditSubjectForm()
    return render(request,'accounts/admin/edit_subjects.html',{'form':form})

def delete_subject(request,subject_id):
    subject = Subjects.objects.filter(id=subject_id)
    try:
        subject.delete()
        messages.request(request,'Subject has been deleted')
        return redirect('accounts:all_subject')
    except:
        messages.request(request,'An error occured try again later')
        return redirect('accounts:all_subjects')

def all_subjects(request):
    subjects = Subjects.objects.all()
    return render(request,'accounts/admin/all_subjects.html',{'subjects':subjects})

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
 
    context={
        "user": user
    }
    return render(request, 'accounts/admin/admin_profile.html', context)

def edit_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    admin = AdminHod.objects.get(id=user)
    if request.method == 'POST':
        form = AddminForm(request.POST,request.FILES,instance=admin,initial={
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
            messages.success(request,'Your Profile has been updated successfully')
    else:
        form = AddminForm()
    return render(request,'accounts/admin/edit_admin_profile.html',{'form':form})