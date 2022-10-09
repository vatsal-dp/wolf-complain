from django.contrib import admin
from django.urls import path
from . import views


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
    path('admin/complain_history/', views.complain_history, name='complain_history'),
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
    path('admin/delete/', views.delete, name='deleteadmin'),
    path('about/', views.about, name='about'),
    path('admin/transfer/<int:cid>/', views.transfer, name='transfer'),
    path('admin/principalComplains/', views.principalComplains, name='principalComplains'),
    path('admin/principalDashboard/', views.principaldashboard, name='principaldashboard'),
    path('admin/members_list', views.memberslist, name='members_list'),
    path('admin/members_list/issue_warning/<int:myid>/', views.issue_warning, name='issue_warning'),
    path('student/complain/likecomplain/',views.likecomplain,name='likecomplain'),
    path('student/complain/collegefeed/',views.collegefeed,name='collegefeed'),



]
