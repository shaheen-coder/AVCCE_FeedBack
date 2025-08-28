from django.db import models


DEPT = (
    ('CSE','be-cse'),
    ('IT','btech-it'),
    ('EEE','be-eee'),
    ('ICE','be-ice'),
    ('ECE','be-ece'),
    ('MECH','be-mech'),
    ('CIVIL','be-civil')
)

# staff model 
class Staff(models.Model):
    GENDER = (
        (1,'male'),
        (0,'female')
    )
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=20,choices=DEPT)
    gender = models.BooleanField(choices=GENDER)
    def __str__(self):
        return f'{self.name[:5]} - {self.dept}'


class Subject(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(primary_key=True,max_length=7)
    dept = models.CharField(max_length=10,choices=DEPT)
    semester = models.SmallIntegerField()
    course_type = models.CharField(max_length=3,default='N')
    
    def __str__(self):
        return f' {self.name[:7]} - {self.code}'


class ClassStaff(models.Model):
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    section = models.CharField(max_length=1)
    semester = models.SmallIntegerField()
    dept = models.CharField(max_length=10,choices=DEPT)
    class Meta:
        verbose_name = "class handling"
    
    def save(self,*args,**kwargs):
        self.section = str(self.section).upper()
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.staff.name} - {self.subject.code}'
    
class TimeScheduler(models.Model):
    start_time = models.DateField()
    end_time = models.DateField()
    dept = models.CharField(max_length=10,choices=DEPT)
    feed = models.IntegerField()
    def clean(self):
        super().clean()
        if self.feed > 2 :
            raise ValidationError("feedback only for 2 times")
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f'feedback : {self.feed} ({self.start_time} - {self.end_time})'