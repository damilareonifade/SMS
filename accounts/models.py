from secrets import choice
from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN','Admin'
        STUDENTS = 'STUDENTS','Student'
        TEACHER = 'TEACHER','Teacher'
     
    role = models.CharField(max_length=20,choices= Role.choices,blank=False,null=False)


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_name= models.CharField(max_length=250)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

    class Meta:
        ordering = ('session_start_year',) 
        verbose_name_plural = ('Session Year Model')
        verbose_name = ('Session Year')
    
    def __str__(self):
        return self.session_name

class AdminHod(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = ('Administrative')
        verbose_name =('Administrative')
        
    def __str__(self):
        return self.admin.username

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = ('Staff')
        verbose_name= ('Staff')
        
    def __str__(self):
        return self.admin.username

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    courses = models.CharField(max_length=250,unique=True)
    course_HOD = models.ForeignKey(Staffs,blank=True,null=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ('courses',)
        verbose_name_plural = ('Courses')
        verbose_name = ('Course')
    
    def __str__(self):
        return self.courses

class Subjects(models.Model):
    LEVEL = (('ND1','ND1'),('ND2','ND2'),('HND1','HND1'),('HND2','HND2'))
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=250)
    level = models.CharField(max_length=200,choices = LEVEL)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staff = models.ForeignKey(Staffs,on_delete=models.CASCADE)

    class Meta:
        ordering = ('subject',)
        verbose_name_plural = ('Subjects')
        verbose_name = ('Subject')

    def __str__(self):
        return self.subject

class Student(models.Model):
    GENDER = (('MALE','Male'),('FEMALE','Female'))
    LEVEL = (('ND1','ND1'),('ND2','ND2'),('HND1','HND1'),('HND2','HND2'))
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50,choices=GENDER)
    profile_pics = models.ImageField(upload_to="media/",blank=True,null=True)
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.CASCADE)
    level = models.CharField(max_length=30,editable=True,choices=LEVEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    class Meta:
        ordering = ('created_at',)
        verbose_name = ('Student')
        verbose_name_plural = ('Students')
        
    def __str__(self):
        return self.admin.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'ADMIN':
            AdminHod.objects.create(admin=instance)
        if instance.role == 'TEACHER':
            Staffs.objects.create(admin=instance)
        if instance.role == 'STUDENTS':
            Student.objects.create(admin=instance,
                                    course_id=Courses.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    address="",
                                    profile_pics="",
                                    gender="")

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.subject_id.subject

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
 
 
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager() 


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.student_id.admin.username

class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.student_id.admin.username
 
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.role == 'ADMIN':
#         instance.adminhod.save()
#     if instance.role == 'TEACHER':
#         instance.staffs.save()
#     if instance.role == 'STUDENTS':
#         instance.students.save()