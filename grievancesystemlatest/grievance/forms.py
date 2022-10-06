from django import forms
from .models import Complain,Admin,Student
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserFormAdmin(UserCreationForm):
    
    email = forms.CharField(max_length=30, label='Email-id')
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    
    class Meta():
        model = User
        fields = [ 'first_name','last_name','username','email',  'password1', 'password2']


class UserFormStudent(UserCreationForm):
    
    email = forms.CharField(max_length=30, label='Email-id')
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    
    class Meta():
        model = User
        fields = [ 'first_name','last_name','email', 'username', 'password1', 'password2']

class ComplainForm(forms.ModelForm):
    class Meta:
        
        model = Complain
        fields=['complain_heading','complain_content', 'college']



class LoginForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password",widget = forms.PasswordInput)

class ChangeStatusForm(ModelForm):
    status_choices = {
        ('Pending', 'Pending'),
        ('Viewed', 'Viewed'),
        ('Solved', 'Solved'),
        ('Rejected', 'Rejected')
    }
    
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=status_choices)
    class Meta:
        model = Complain
        fields=['status','response']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        
        model = Student
        fields=['college','branch']

class AdminProfileForm(forms.ModelForm):
    class Meta:
        
        model = Admin
        fields=['college']
        
        
class EditStudent(ModelForm):
    class Meta:
        model = Student
        fields = ['college', 'branch']

class EditUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
class EditAdmin(ModelForm):
    class Meta:
        model = Admin
        fields = ['designation', 'college', 'branch']        