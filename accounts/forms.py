from re import A
from tabnanny import verbose

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (AdminHod, Courses, CustomUser, FeedBackStudent,
                     LeaveReportStaff, LeaveReportStudent, SessionYearModel,
                     Staffs, Student, StudentResult, Subjects)


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','password1','password2',]

    def username(self):
        username = self.cleaned_data["username"]
        user = CustomUser.objects.filter(username=username).exists()
        if user is True:
            raise forms.ValidationError('You can\'t use this username try another one')
        return username

    def email(self):
        email = self.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email).exists()
        if user is True:
            raise forms.ValidationError('You can\'t use this email')            
        return email


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(label='First name',max_length=250)
    last_name = forms.CharField(label='Last name',max_length=250)
    username = forms.CharField(max_length=250)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['gender','profile_pics','address','course_id']
        

class AddStudentForm(forms.ModelForm):
    username = forms.CharField(label='Username',max_length=250,)
    first_name = forms.CharField(label='First name',max_length=250)
    last_name = forms.CharField(label='Last name',max_length=250)
    email = forms.EmailField()
    password = forms.CharField(label='Password',widget=forms.PasswordInput(),max_length=250,min_length=8)
    class Meta:
        model = Student
        fields = ['course_id','gender','address','profile_pics','course_id','session_year_id','level']


class AddStaffForm(forms.ModelForm):
    username = forms.CharField(label='Username',max_length=250,help_text='Note Username is unique')
    first_name = forms.CharField(label='First name',max_length=250)
    last_name = forms.CharField(label='Last name',max_length=250)
    email = forms.EmailField()
    password = forms.CharField(label='Password',widget=forms.PasswordInput(),max_length=250,min_length=8)

    class Meta:
        model = Staffs
        fields = ['address']

class EditStaffForm(forms.ModelForm):
    username = forms.CharField(label='name',max_length=250,help_text='Note Username is unique')
    first_name = forms.CharField(label='First name',max_length=250)
    last_name = forms.CharField(label='Last name',max_length=250)
    email = forms.EmailField()

    class Meta:
        model = Staffs
        fields = ['address']

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['courses']

class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['courses']

class SessionYearForm(forms.ModelForm):
    model = SessionYearModel
    fields = ['session_name','session_start_year','session_end_year']


class SessionYearEditForm(forms.ModelForm):
    model = SessionYearModel
    fields = ['session_name','session_start_year','session_end_year']

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['subject','course','level','staff']

class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['subject','course','level','staff']

class AddminForm(forms.ModelForm):
    username = forms.CharField(label='name',max_length=250,help_text='Note Username is unique')
    first_name = forms.CharField(label='First name',max_length=250)
    last_name = forms.CharField(label='Last name',max_length=250)
    email = forms.EmailField()

    class Meta:
        model = AdminHod
        fields = ['address']

class LeaveNewForm(forms.ModelForm):
    class Meta:
        model = LeaveReportStudent
        fields = ['leave_date','leave_message']

class StudentFeedBackForm(forms.ModelForm):
    class Meta:
        model =  FeedBackStudent
        fields = ['feedback']
        

class StaffLeaveForm(forms.ModelForm):
    class Meta:
        model =LeaveReportStaff
        fields = ['leave_date','leave_message','leave_status']


class StudentReportForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        fields = ['subject_exam_marks','subject_assignment_marks']

class LoginForm(forms.Form):
    username=forms.CharField(max_length=250,label='Username')
    password = forms.CharField(max_length=25,label='Password')