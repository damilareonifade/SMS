from django.db import models

from accounts.models import SessionYearModel


class Finance(models.Model):
    name = models.CharField(max_length=250,default='School Feesst')
    amount = models.IntegerField()
    other_fees = models.IntegerField(blank=True,null=True)
    session_year = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Finance'
        verbose_name_plural='Finance'


class Courses(models.Model):
    LEVEL = (('ND1','ND1'),('ND2','ND2'),('HND1','HND1'),('HND2','HND2'))
    id = models.AutoField(primary_key=True)
    courses = models.CharField(max_length=250,unique=True)
    level = models.CharField(max_length=250,choices = LEVEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ('courses',)
        verbose_name_plural = ('Courses')
        verbose_name = ('Course')
    
    def __str__(self):
        return self.courses

class Student(models.Model):
    GENDER = (('MALE','Male'),('FEMALE','Female'))
    LEVEL = (('ND1','ND1'),('ND2','ND2'),('HND1','HND1'),('HND2','HND2'))
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50,choices=GENDER)
    profile_pics = models.ImageField(upload_to="media/",blank=True,null=True)
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.CASCADE,related_name='student_session_year')
    level = models.CharField(max_length=30,editable=True,choices=LEVEL)
    fees = models.ManyToManyField(Finance,related_name='student_fees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey('Role',on_delete=models.CASCADE,null=True,blank=True)
    objects = models.Manager()
    class Meta:
        ordering = ('created_at',)
        verbose_name = ('Student')
        verbose_name_plural = ('Students')
        
    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
