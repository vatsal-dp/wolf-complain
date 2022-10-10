from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    college_choices=(
        ('DJ Sanghvi College of Engineering','DJ Sanghvi College of Engineering'),
        ('KJ Somaiya College of Engineering','KJ Somaiya College of Engineering'),
        ('Thadomal Sahani College of Engineering','Thadomal Sahani College of Engineering'),
        ('Thakur College of Engineering','Thakur College of Engineering'),
        ('Atharva College of Engineering','Atharva College of Engineering'),
        ('Sardar Patel College of Engineering','Sardar Patel College of Engineering'),
        ('VJTI College of Engineering','VJTI College of Engineering'),
    )

    branch_choices=(
        ('Computer','Computer'),
        ('IT','IT'),
        ('EXTC','EXTC'),
        ('ELEX','ELEX'),
        ('Chemical','Chemical'),
        ('Production','Production'),
        ('Bio Med','Bio Med')

    )

    designation_choices = {
        ('Principal', 'Principal'),
        ('Vice-Principal', 'Vice-Principal'),
        ('HOD', 'HOD'),
        ('Senior Librarian', 'Senior Librarian'),
        ('Security Head', 'Security Head'),
        ('Canteen Owner', 'Canteen Owner')   
    }
    
   
    
    
    user = models.OneToOneField(User,default='',on_delete=models.CASCADE)
    college=models.CharField(max_length=300,default='',choices=college_choices)
    branch=models.CharField(max_length=300, blank='true',null='true',choices=branch_choices)
    designation = models.CharField(max_length=20, default='', choices=designation_choices)


    def __str__(self):
        return f"{self.user.username}, Department : {self.branch}"



class Student(models.Model):
    college_choices=(
        ('DJ Sanghvi College of Engineering','DJ Sanghvi College of Engineering'),
        ('KJ Somaiya College of Engineering','KJ Somaiya College of Engineering'),
        ('Thadomal Sahani College of Engineering','Thadomal Sahani College of Engineering'),
        ('Thakur College of Engineering','Thakur College of Engineering'),
        ('Atharva College of Engineering','Atharva College of Engineering'),
        ('Sardar Patel College of Engineering','Sardar Patel College of Engineering'),
        ('VJTI College of Engineering','VJTI College of Engineering'),
    )

    branch_choices=(
        ('Computer','Computer'),
        ('IT','IT'),
        ('EXTC','EXTC'),
        ('ELEX','ELEX'),
        ('Chemical','Chemical'),
        ('Production','Production'),
        ('Bio Med','Bio Med'),

    )

    user = models.OneToOneField(User,on_delete=models.CASCADE,default='')
    college=models.CharField(max_length=300,default='',choices=college_choices)
    branch=models.CharField(max_length=300,default='',choices=branch_choices)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg', verbose_name='Profile Picture')


    def __str__(self):
        return f"{self.user.username} : {self.branch}'s Student"


class Complain(models.Model):
    college_choices=(
        ('DJ Sanghvi College of Engineering','DJ Sanghvi College of Engineering'),
        ('KJ Somaiya College of Engineering','KJ Somaiya College of Engineering'),
        ('Thadomal Sahani College of Engineering','Thadomal Sahani College of Engineering'),
        ('Thakur College of Engineering','Thakur College of Engineering'),
        ('Atharva College of Engineering','Atharva College of Engineering'),
        ('Sardar Patel College of Engineering','Sardar Patel College of Engineering'),
        ('VJTI College of Engineering','VJTI College of Engineering'),
    )

    branch_choices=(
        ('Computer','Computer'),
        ('IT','IT'),
        ('EXTC','EXTC'),
        ('ELEX','ELEX'),
        ('Chemical','Chemical'),
        ('Production','Production'),
        ('Bio Med','Bio Med')

    )
    
    status_choices = {
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Viewed', 'Viewed'),
        ('Solved', 'Solved'),
        ('Rejected', 'Rejected')
    }
    
   
    related_to_choices={
        ('Management', 'Management'),
        ('Faculty', 'Faculty'),
        ('Security', 'Security'),
        ('Library', 'Library'),
        ('Canteen', 'Canteen')
    }
    complain_heading=models.CharField(max_length=300,default='')
    complain_content=models.TextField()
    receiver=models.ForeignKey(Admin,on_delete=models.CASCADE, null = True)
    sender=models.ForeignKey(Student,on_delete=models.CASCADE, null = True)
    college=models.CharField(max_length=300,default='',choices=college_choices)
    branch=models.CharField(max_length=300,blank='true', null='true',choices=branch_choices)
    date_posted =models.DateTimeField(default=timezone.now, null = True)
    date_resolved = models.CharField(default='', max_length = 40, null = True)
    status = models.CharField(choices = status_choices, default='Pending', max_length = 20)
    response = models.TextField(default='')
    related_to = models.CharField(choices = related_to_choices, default='', max_length = 20, verbose_name = 'Complain Related to')
    transfer = models.BooleanField(default=False)
    likes=models.ManyToManyField(User,related_name='complain')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.college} : {self.branch}"


    class Meta:
        ordering=['-date_posted']

class Like(models.Model):
    complain=models.ForeignKey(Complain,on_delete=models.CASCADE,default='',related_name='complain')
    liker=models.ForeignKey(Student,on_delete=models.CASCADE,default='')



class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone