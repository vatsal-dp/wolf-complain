import pytest
from urllib import request
from django.test import TestCase
from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth.models import User

def test_main_page():
    assert (render(request, 'grievance/home.html').status_code ==200)

@pytest.mark.django_db(transaction = True)
def test_create_compain():
    complain = Complain.objects.create(
    complain_heading="test_complain",
    complain_content="................",
    college = 'DJ Sanghvi College of Engineering',
    branch = 'Computer',
    # date_posted = timezone.now,
    # date_resolved = timezone.now,
    status = 'Solved',
    response = 'Done',
    related_to = 'Management',
    transfer = False,

    )    

    assert complain.college == "DJ Sanghvi College of Engineering"
    
@pytest.mark.django_db(transaction = True)
def test_create_user():
    global user_t
    user_t = User.objects.create_user(username="test_user", password="test")

    assert user_t.username == 'test_user'

@pytest.mark.django_db(transaction = True)
def test_create_student():
    user_1 = User.objects.create_user(username="test_user", password="test")
    student = Student.objects.create(
        user = user_1,
        college = 'DJ Sanghvi College of Engineering',
        branch = 'Computer'
    )

    assert student.college == 'DJ Sanghvi College of Engineering'
    assert student.branch == 'Computer'

@pytest.mark.django_db(transaction = True)
def test_create_admin():
    user_1 = User.objects.create_user(username="test_user", password="test")
    admin = Admin.objects.create(
        user = user_1,
        college = 'DJ Sanghvi College of Engineering',
        branch = 'Computer'
    )

    assert admin.college == 'DJ Sanghvi College of Engineering'
    assert admin.branch == 'Computer'