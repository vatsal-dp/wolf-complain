from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('',views.home,name='home'),
    path('register/admin/',views.adminRegister,name='adminRegister'),
    path('register/student/',views.studentRegister,name='studentRegister'),
    path('login/student/',views.loginStudent,name='loginStudent'),
    path('login/admins/',views.loginAdmin,name='loginAdmin'),
    path('student/studentdashboard/',views.studentdashboard,name='studentdashboard'),
    path('admin/admindashboard/',views.admindashboard,name='admindashboard'),
    path('admin/admindashboard/profile/',views.adminProfileView,name='adminProfileView'),
    path('adminComplainView/<int:cid>/',views.adminComplainView,name='adminComplainView'),
    path('student/studentdashboard/AddComplain/',views.addComplain,name='addComplain'),
    path('student/studentdashboard/previousComplaints/',views.previousComplaints,name='previousComplaints'),
    path('student/studentdashboard/studentProfileView/',views.studentProfileView,name='studentProfileView'),
    path('studentComplainView/<int:cid>/',views.studentComplainView,name='studentComplainView'),
    path('complainview/<int:cid>/', views.complainview, name='complainview'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin/completeprofile/', views.adminProfile, name='adminProfile'),
    path('student/completeprofile/', views.studentProfile, name='studentProfile'),
    path('student/activate/<uidb64>/<token>/<name>/', views.activatestudent, name='activatestudent'),
    path('admin/activate/<uidb64>/<token>/<name>/', views.activateadmin, name='activateadmin'),
    path('student/studentdashboard/studentProfileView/editprofile/', views.student_editprofile, name='student_editprofile'),
    path('admin/admindashboard/profile/editprofile/', views.admin_editprofile, name='admin_editprofile'),
    path('student/delete/', views.delete, name='deletestudent'),
    path('admin/delete/', views.delete, name='deleteadmin')


]