from django.shortcuts import render,redirect,reverse,HttpResponse
from.models import Complain,Admin,Student,Like
from.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from .decorators import *
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.encoding import force_str

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from datetime import datetime
from datetime import date
import calendar
import requests
from operator import itemgetter


def likecomplain(request):

    cid=request.GET.get('cid')
    complain=Complain.objects.get(id=cid)
    if complain.likes.filter(id = request.user.id).exists() :
        complain.likes.remove(request.user)
    else:
        complain.likes.add(request.user)
    return redirect('collegefeed')

# Create your views here.
def home(request):
   # group=Group.objects.get(user=request.user)


    return render(request,'grievance/home.html')

@is_logged
def adminRegister(request):
    if request.method=='POST':
        form=UserFormAdmin(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            name = user.username
            user.is_active = True
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            for x in User.objects.all():
                if x.email == email:
                    messages.info(request, f'Account with this email already exists.')
                    return redirect('adminRegister')
            user.save()
            group=Group.objects.get(name='faculty')
            user.groups.add(group)
            current_site = get_current_site(request)                #Email activation
            mail_subject = 'Activate your admin account.'
            message = render_to_string('grievance/acc_adminactive_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'name':name
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, 'Please confirm your email address to complete the registration')   #Email activation end
            return redirect('loginAdmin')
    else:
        form=UserFormAdmin()
    return render(request,'grievance/registeradmin.html',{'form':form})

def activateadmin(request, uidb64, token, name):
    try:
        uid = force_str((urlsafe_base64_decode(uidb64)))
        user = User.objects.get(pk=uid)
        print(uid)
    except Exception as identifier:
        print(uid)
        print(uidb64)
        user = User.objects.get(username=name)
    if user is not None and account_activation_token.check_token(user, token):
        print('Success')
        user.is_active = True
        user.save()
        group=Group.objects.get(name='faculty')
        user.groups.add(group)
        messages.info(request, f'Thank you for your email confirmation. Your account has been created! {user.username}, you are now ready to Log In.')
        return redirect('loginAdmin')
    else:
        user.delete()
        messages.info(request, 'Activation link is invalid! Request account activation again')
        return redirect('adminRegister')

@is_logged
def studentRegister(request):
    if request.method=='POST':
        form=UserFormStudent(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active = True
            name = user.username
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            for x in User.objects.all():
                if x.email == email:
                    messages.info(request, f'Account with this email already exists.')
                    return redirect('studentRegister')

            user.save()
            group=Group.objects.get(name='student')
            user.groups.add(group)
            print(user.id)
            current_site = get_current_site(request)                #Email activation
            mail_subject = 'Activate your student account.'
            message = render_to_string('grievance/acc_studentactive_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'name':name
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, 'Please confirm your email address to complete the registration')   #Email activation end
            return redirect('loginStudent')
    else:
        form=UserFormStudent()
    return render(request,'grievance/registerstudent.html',{'form':form})

@is_logged
def loginStudent(request):
    if request.method=='POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username,password = password)
            if user is not None:
                group=Group.objects.get(user=user)
                g=group.name
                if g == 'student':
                    login(request,user)
                    return redirect('studentdashboard')
                else:
                    messages.info(request, f'Account belongs to a faculty. Go to the admin login page and Log In')
            elif user is None:
                messages.info(request, f'Invalid Credentials.')
    else:
        form= LoginForm()
    return render(request,"grievance/studentlogin.html",{'form':form})

@is_logged
def loginAdmin(request):
    if request.method=='POST':
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username,password = password)
            if user is not None:
                group=Group.objects.get(user=user)
                g=group.name
                if g == 'faculty':
                    login(request,user)
                    profile=Admin.objects.filter(user=request.user).count()
                    if profile>0:
                        if request.user.admin.designation == 'Principal':
                            return redirect('principaldashboard')
                        else:
                            return redirect('admindashboard')
                    else:
                        return redirect("adminProfile")




                else:
                    messages.info(request, f'Account belongs to a student. Go to the student login page and Log In')
            elif user is None:
                messages.info(request, f'Invalid Credentials.')

    else:
        form= LoginForm()
    return render(request,"grievance/adminlogin.html",{'form':form})



@login_required(login_url='/login/student/')
@student_required
@studentprofile_required
def studentComplainView(request,cid):
    complain=Complain.objects.get(id=cid)
    context={
        'complain':complain,
        'scomplains_active':'active'
    }
    return render(request,'grievance/studentComplainView.html',context)


def activatestudent(request, uidb64, token, name):
    try:
        uid = force_str((urlsafe_base64_decode(uidb64)))
        user = User.objects.get(pk=uid)
        print(uid)
    except Exception as identifier:
        print(uid)
        print(uidb64)
        user = User.objects.get(username=name)
    if user is not None and account_activation_token.check_token(user, token):
        print('Success')
        user.is_active = True
        user.save()
        group=Group.objects.get(name='student')
        user.groups.add(group)
        messages.info(request, f'Thank you for your email confirmation. Your account has been created! {user.username}, you are now ready to Log In.')
        return redirect('loginStudent')
    else:
        user.delete()
        messages.info(request, 'Activation link is invalid! Request account activation again')
        return redirect('studentRegister')


@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def adminComplainView(request,cid):
    complain = Complain.objects.get(id = cid)
    status = complain.status
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST, instance=complain)
        instance = form.save(commit=False)
        complain.status = instance.status
        complain.date_resolved = date.today().strftime('%b %d, %Y')
        complain.save()
        # if complain.status == 'In Progress':
        #     mail_subject = 'Complain in progress'
        #     message =  'Hey ' +complain.sender.user.first_name+',\nYour complain is in progress and will be addressed very soon.\n\nYour complain details.\nComplain heading : '+complain.complain_heading+'\nComplain content: '+complain.complain_content+'\nResponse provided: '+complain.response
        # else:
        #     mail_subject = 'Complain '+complain.status
        #     message =  'Hey ' +complain.sender.user.first_name+',\nYour complain was '+complain.status+' by the concerned authority.\n\nYour complain details.\nComplain heading : '+complain.complain_heading+'\nComplain content: '+complain.complain_content+'\nResponse provided: '+complain.response
        # to_email = complain.sender.user.email
        # email = EmailMessage(
        #             mail_subject, message, to=[to_email]
        # )
        # email.send()
        messages.info(request, f'Status changed successfully!')
        if request.user.admin.designation == 'Principal':
            return redirect('principaldashboard')
        else:
            return redirect('admindashboard')
    else:
        form = ChangeStatusForm(instance=complain)
    return render(request, 'grievance/adminComplainView.html', {'form':form, 'complain':complain, 'admin_complains_active':'active'})

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def adminProfileView(request):
    admin=Admin.objects.get(user=request.user)
    tcomplains=Complain.objects.filter(receiver=admin).count()
    rcomplains=Complain.objects.filter(receiver=admin,status='Rejected').count()
    scomplains=Complain.objects.filter(receiver=admin,status='Solved').count()
    context={
        'a':admin,
        'scomplains':scomplains,
        'rcomplains':rcomplains,
        'tcomplains':tcomplains,
        'admin_profile_active':'active'

    }
    return render(request,'grievance/adminProfileView.html',context)

@login_required(login_url='/login/student/')
@student_required
@studentprofile_required
def studentProfileView(request):
    student=Student.objects.get(user=request.user)
    tcomplains=Complain.objects.filter(sender=student).count()
    rcomplains=Complain.objects.filter(sender=student,status='Rejected').count()
    scomplains=Complain.objects.filter(sender=student,status='Solved').count()
    context={
        'a':student,
        'scomplains':scomplains,
        'rcomplains':rcomplains,
        'tcomplains':tcomplains,
        'sprofile_active':'active'

    }
    return render(request,'grievance/studentProfileView.html',context)

@login_required(login_url='/login/student/')
@student_required
@studentprofile_required
def student_editprofile(request):
    student = Student.objects.get(user = request.user)
    user = request.user
    if request.method == 'POST':
        u_form = EditUser(request.POST, instance=user)
        s_form = EditStudent(request.POST, request.FILES, instance=student)
        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.info(request, 'Profile Updated Successfully!')
            return redirect('studentProfileView')
    else:
        u_form = EditUser(instance=user)
        s_form = EditStudent(instance=student)
    return render(request, 'grievance/student_editprofile.html', {'form1':u_form, 'form2':s_form, 'sprofile_active':'active'})

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def principalComplains(request):
    pcollege = request.user.admin.college
    admin = Admin.objects.get(college = pcollege, designation = 'Principal')
    vcomplains = Complain.objects.filter(Q(college = pcollege,transfer = True, status = 'Viewed') | Q(college = pcollege, status = 'Pending', receiver = admin) | Q(college = pcollege, receiver = admin, status = 'Viewed'))
    for x in vcomplains:
        if x.status == 'Pending':
            x.status = 'Viewed'
            x.save()
    srtcomplains =  Complain.objects.filter(Q(status = 'Solved', college = pcollege,transfer = True, ) | Q(status = 'Rejected', college = pcollege,transfer = True, ) | Q(status = 'In Progress', college = pcollege,transfer = True, ) | Q(college = pcollege, status = 'Solved', receiver = admin) | Q(college = pcollege, status = 'Rejected', receiver = admin) | Q(college = pcollege, status = 'In Progress', receiver = admin))
    context={
        'vcomplains' : vcomplains,
        'my_complains' : 'active',
        'srtcomplains' : srtcomplains
    }
    return render(request,'grievance/principalComplains.html',context)

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def admin_editprofile(request):
    admin = Admin.objects.get(user = request.user)
    user = request.user
    if request.method == 'POST':
        u_form = EditUser(request.POST, instance=user)
        a_form = EditAdmin(request.POST, instance=admin)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.info(request, 'Profile Updated Successfully!')
            return redirect('adminProfileView')
    else:
        u_form = EditUser(instance=user)
        a_form = EditAdmin(instance=admin)
    return render(request, 'grievance/admin_editprofile.html', {'form1':u_form, 'form2':a_form, 'admin_profile_active':'active'})

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def complain_history(request):
    admin = Admin.objects.get(user = request.user)
    complains = Complain.objects.filter(receiver = admin)
    return render (request, 'grievance/admin_complain_history.html', {'complains':complains, 'admin_complains_active':'active'})

'''def like(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        student = Student.objects.get(user = request.user)
        complain1 = Complain.objects.get(id = cid )
        new_like,created = Like.objects.get_or_create(liker = student ,complain = complain1)
        if not created:
            new_like.save()

            return redirect('previousComplaints')
        else:
            complain1.like_count = complain1.like_count+1
            complain1.save()
            return redirect('previousComplaints')'''

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def memberslist(request):
    admin = Admin.objects.filter(college = request.user.admin.college)
    return render(request, 'grievance/members_list.html', {'members_list':'active', 'admins':admin})



def delete(request):
    user = request.user
    user.delete()
    messages.info(request, 'Account deleted successfully!')
    return redirect('home')

def about(request):
    return render (request, 'grievance/about.html')

def transfer(request,cid):
    if request.method == 'POST':
        complain = Complain.objects.get(id = cid)
        complain.transfer = True
        complain.save()
        messages.info(request, 'Complain transferred to higher authority!')
        return redirect('admindashboard')

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def principaldashboard(request):
    complains=Complain.objects.filter(college=request.user.admin.college)
    compcomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='Computer',college=request.user.admin.college)
    itcomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='IT',college=request.user.admin.college)
    chemcomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='Chemical',college=request.user.admin.college)
    extccomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='EXTC',college=request.user.admin.college)
    elexcomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='Elex',college=request.user.admin.college)
    prodcomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='Production',college=request.user.admin.college)
    biocomplains=Complain.objects.filter(date_posted__gte=timezone.now().replace(day=1, hour=0,minute=0,second=0,microsecond=0),branch='Bio Med',college=request.user.admin.college)

    months = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0,
        11:0,
        12:0,
    }



    c=datetime.today()
    cm=c.month
    cm1=c.month
    diff= cm1 - 6

    cy=c.year
    cy1=c.year


    for i in range(0,6) :
        if cm < 1:
            cm=12
            cy=cy-1
        for x in complains:
            l = str(x.date_posted)
            monthnumber = l[5:7]
            m=int(monthnumber)
            year = l[0:4]
            y=int(year)
            if m == cm and y == cy:
                months[cm] = months[cm] + 1
        cm = cm-1

    context={
        'compcomplains':compcomplains,
        'itcomplains':itcomplains,
        'extccomplains':extccomplains,
        'elexcomplains':elexcomplains,
        'prodcomplains':prodcomplains,
        'biocomplains':biocomplains,
        'chemcomplains':chemcomplains,
        'cy1':cy1,
        'cm1':cm1,
        'cy':cy,
        'diff':diff,
        'months':months,
        'pcomplains' : 'active'
    }

    return render(request,'grievance/principaldashboard.html',context)

@login_required(login_url='/login/student/')
@student_required
@studentprofile_required
def collegefeed(request):
    if request.method == 'POST':
        college = request.POST.get('college')
        type = request.POST.get('type')
        department = request.POST.get('department')
        print(college, type, department)
        if college == '' and type == '' and department == '':
            complains=Complain.objects.all()
        else:

            if college != '':
                complains = Complain.objects.filter( college = college)
                if type != '':
                    complains = complains.filter(related_to = type)
                    type = ''
                    if department != '':

                        complains = complains.filter(branch = department)
                        department = ''

            if type != '':
                    complains = Complain.objects.filter(related_to = type)
                    if department != '':
                        complains = complains.filter(branch = department)
                        department = ''
            if department != '':
                        complains = Complain.objects.filter(branch = department)
    else:
        complains=Complain.objects.all()
    college_list =   [ 'NCSU', 'TAMU', 'USC', 'NYU', 'UIUC', 'UCSD', 'CMU'     ]
    type = ['Management', 'Library', 'Faculty', 'Security']
    department = ['Computer',
        'IT',
        'EXTC',
        'ELEX',
        'Chemical',
        'Production',
        'Bio Med']

    p = Paginator(complains, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    print(page_obj.number)
    context={
        'complains':page_obj,
        'collegefeed_active':'active',
        'college_list' : college_list,
        'type' : type,
        'department':department,
    }
    return render(request,'grievance/collegefeed.html',context)

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def issue_warning(request, myid):
        admin = Admin.objects.get(user = myid)
        mail_subject = 'Warning'
        message = 'This email has been sent to you to bring in to your notice that many complains have been written into your department. Please look after it.\n\nPrincipal.'
        # to_email = admin.user.email
        # email = EmailMessage(
        #         mail_subject, message, to=[to_email]
        # )
        # email.send()
        messages.info(request, 'Warning issued successfully!')
        return redirect('members_list')
