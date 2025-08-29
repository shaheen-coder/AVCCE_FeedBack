from django.contrib.auth.models import AbstractUser
from django.db import models
#other models 
from staff.models import ClassStaff
from staff.models import Staff,Subject
# custom user 
class AdminUser(AbstractUser):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('hod', 'Head of Department'),
        ('principal', 'Principal'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dept = models.CharField(max_length=100, blank=True, null=True)  
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)
    def is_staff_user(self):
        return self.role == 'staff'

    def is_hod_user(self):
        return self.role == 'hod'

    def is_principal_user(self):
        return self.role == 'principal'

DEPT = (
    ('CSE','be-cse'),
    ('IT','btech-it'),
    ('EEE','be-eee'),
    ('ICE','be-ice'),
    ('ECE','be-ece'),
    ('MECH','be-mech'),
    ('CIVIL','be-civil'),
    ('AIDS','be-aids'),
)
# student base model 
class StudentBase(models.Model):
    regno = models.BigIntegerField(primary_key=True)
    dob = models.DateField()
    name = models.CharField(max_length=30)
    gender = models.BooleanField()
    dept = models.CharField(max_length=5,choices=DEPT)
    active = models.BooleanField(default=True)
    batch = models.CharField(max_length=5)    
    def __str__(self):
        return f'{self.name[:7]} - {self.dept}'
# students 
class Student(models.Model):
    student = models.ForeignKey(StudentBase,on_delete=models.CASCADE)
    section = models.CharField(max_length=1)
    semester = models.SmallIntegerField() 
    feed1_status = models.BooleanField(default=False,null=True,blank=True)
    feed2_status = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return f'{self.student.name[:7]} - {self.student.dept}:{self.section}'



class FeedBack(models.Model):
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(StudentBase,on_delete=models.CASCADE)
    batch = models.CharField(max_length=5)
    semester = models.SmallIntegerField()
    section = models.CharField(max_length=1)
    dept = models.CharField(max_length=5,choices=DEPT)
    feed1 = models.JSONField(null=True,blank=True)
    feed2 = models.JSONField(null=True,blank=True)
    msg = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return f'{self.staff.id} - {self.subject.code} - {self.student.regno}'