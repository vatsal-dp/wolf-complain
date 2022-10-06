from django.shortcuts import render,redirect,reverse,HttpResponse
from.models import Complain,Admin,Student
from.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *



from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage





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
            user.is_active = False
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            for x in User.objects.all():
                if x.email == email:
                    messages.info(request, f'Account with this email already exists.')
                    return redirect('adminRegister')
            user.save()
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
            return redirect('adminRegister')    
    else:
        form=UserFormAdmin()
    return render(request,'grievance/registeradmin.html',{'form':form})



def activateadmin(request, uidb64, token, name):
    try:
        uid = force_text((urlsafe_base64_decode(uidb64)))
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
        messages.info(request, f'Thank you for your email confirmation. Your account has been created! {user.first_name}, you are now ready to Log In.')
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
            user.is_active = False
            name = user.username
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            for x in User.objects.all():
                if x.email == email:
                    messages.info(request, f'Account with this email already exists.')
                    return redirect('studentRegister')
            
            user.save()
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
            return redirect('studentRegister')
    else:
        form=UserFormStudent()
    return render(request,'grievance/registerstudent.html',{'form':form})




def activatestudent(request, uidb64, token, name):
    try:
        uid = force_text((urlsafe_base64_decode(uidb64)))
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
        messages.info(request, f'Thank you for your email confirmation. Your account has been created! {user.first_name}, you are now ready to Log In.')
        return redirect('loginStudent')
    else:
        user.delete()
        messages.info(request, 'Activation link is invalid! Request account activation again')
        return redirect('studentRegister')


    
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
                    return redirect('admindashboard')
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
def studentdashboard(request):
    student= Student.objects.get(user=request.user)
    pcomplains=Complain.objects.filter(sender=student,status='Pending')
    rcomplains=Complain.objects.filter(sender=student,status='Rejected')
    vcomplains=Complain.objects.filter(sender=student,status='Viewed')
    scomplains=Complain.objects.filter(sender=student,status='Solved')
    p=pcomplains.count()
    r=rcomplains.count()
    s=scomplains.count()
    v=vcomplains.count()

    context={
        'student':student,
        'pcomplains':pcomplains,
        'vcomplains':vcomplains,
        'rcomplains':rcomplains,
        'scomplains':scomplains,
        'r':r,
        's':s,
        'p':p,
        'v':v,
    }
    return render(request,'grievance/studentdashboard.html',context)

@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def admindashboard(request):
    admin=Admin.objects.get(user=request.user)
    college = admin.college
    complains=Complain.objects.filter(receiver=admin)
    for c  in complains:
        if c.status == 'Pending':
            c.status = 'Viewed'
            c.save()

    rcomplains=Complain.objects.filter(receiver=admin,status='Rejected')
    scomplains=Complain.objects.filter(receiver=admin,status='Solved')
    vcomplains=Complain.objects.filter(receiver=admin,status='Viewed')
    management = Complain.objects.filter(college=college, related_to='Management').count()
    security = Complain.objects.filter(college=college, related_to='Security').count()
    library = Complain.objects.filter(college=college, related_to='Library').count()
    faculty = Complain.objects.filter(college=college, related_to='Faculty').count()
    canteen = Complain.objects.filter(college=college, related_to='Canteen').count()
    computer = Complain.objects.filter(college=college, related_to='Faculty', branch='Computer').count()
    it = Complain.objects.filter(college=college, related_to='Faculty', branch='IT').count()
    extc = Complain.objects.filter(college=college, related_to='Faculty', branch='EXTC').count()
    elex = Complain.objects.filter(college=college, related_to='Faculty', branch='ELEX').count()
    chemical = Complain.objects.filter(college=college, related_to='Faculty', branch='Chemical').count()
    production = Complain.objects.filter(college=college, related_to='Faculty', branch='Production').count()
    biomed = Complain.objects.filter(college=college, related_to='Faculty', branch='Bio Med').count()
    
    months = {
        '01':0,
        '02':0,
        '03':0,
        '04':0,
        '05':0,
        '06':0,
        '07':0,
        '08':0,
        '09':0,
        '10':0,
        '11':0,
        '12':0,    
    }
    for month in months:
        for x in complains:
            l = str(x.date_posted)
            monthnumber = l[5:7]
            if monthnumber == month:
                months[month] = months[month] + 1
    
    context={
        'rcomplains':rcomplains,
        'scomplains':scomplains,
        'vcomplains':vcomplains,
        'months':months,
        'management':management,
        'security':security,
        'library':library,
        'faculty':faculty,
        'canteen':canteen,
        'computer':computer,
        'it':it,
        'extc':extc,
        'elex':elex,
        'chemical':chemical,
        'production':production,
        'biomed':biomed
    }
    return render(request,'grievance/admindashboard.html',context)

@login_required(login_url='/login/student/')
@student_required
@studentprofile_required
def addComplain(request):
    student=Student.objects.get(user=request.user)
    if request.method=='POST':
        form=ComplainForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            college=form.cleaned_data.get('college')
            related_to=request.POST.get('related')
            if related_to == 'Faculty':
                 branch=request.POST.get('branches')
            else:
                branch = None
            
            try:
                        if related_to == 'Management':
                            admin=Admin.objects.filter(college=college, designation='Principal').count()
                        elif related_to == 'Faculty':
                            admin=Admin.objects.filter(college=college,branch=branch, designation='HOD').count()
                        elif related_to == 'Security':
                            admin=Admin.objects.filter(college=college, designation='Security Head').count()
                        elif related_to == 'Library':
                            admin=Admin.objects.filter(college=college, designation='Senior Librarian').count()
                        elif related_to == 'Canteen':
                            admin=Admin.objects.filter(college=college, designation='Canteen Owner').count()    
            except:
                        admin = 0
            if admin!= 0:
                    if related_to == 'Management':
                        admin=Admin.objects.get(college=college, designation='Principal')
                    elif related_to == 'Faculty':
                        admin=Admin.objects.get(college=college,branch=branch, designation='HOD')
                    elif related_to == 'Security':
                        admin=Admin.objects.get(college=college, designation='Security Head')
                    elif related_to == 'Library':
                        admin=Admin.objects.get(college=college, designation='Senior Librarian') 
                    elif related_to == 'Canteen':
                        admin=Admin.objects.filter(college=college, designation='Canteen Owner')    
                    instance.sender=student
                    instance.receiver=admin
                    instance.branch = branch
                    instance.related_to = related_to
                    instance.save()
                    messages.info(request, f'Complain sent to the concerned authority.')
                    return redirect('studentdashboard')
            else:
                     messages.info(request, f"The concerned authority is not available on our system.")
    else:
        form=ComplainForm()
    return render(request,'grievance/addComplain.html',{'form':form})


@login_required(login_url='/login/admins/')
@admin_required
@adminprofile_required
def complainview(request,cid):
    complain = Complain.objects.get(id = cid)
    status = complain.status
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST, instance=complain)
        instance = form.save(commit=False)
        complain.status = instance.status
        complain.save()
        messages.info(request, f'Status changed successfully!')
        return redirect('admindashboard')
    else:
        form = ChangeStatusForm(instance=complain)
    return render(request, 'grievance/complainview.html', {'form':form, 'c':complain})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/student/')
@student_required
def studentProfile(request):
    profile=Student.objects.filter(user=request.user).count()
    if profile>0:
        return redirect('studentdashboard')
    else:
        if request.method=='POST':
            form=StudentProfileForm(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                return redirect('studentdashboard')
        else:
            form=StudentProfileForm()
        return render(request,'grievance/profileStudent.html',{'form':form})


@login_required(login_url='/login/admins/')
@admin_required
def adminProfile(request):
    profile=Admin.objects.filter(user=request.user).count()
    if profile>0:
        return redirect('admindashboard')
    else:
        if request.method=='POST':
            form=AdminProfileForm(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                college = form.cleaned_data.get("college")
                designation = request.POST.get("designation")
                if designation == 'HOD':
                    branch = request.POST.get('branches')
                else:
                    branch = None
                #messages.info(request, f'{branch}')
                #return redirect('adminProfile')
                admin=Admin.objects.filter(college=college,branch=branch, designation=designation).count()
                if admin>0:
                    if branch:
                        messages.info(request, f"Admin account for {branch} branch already exists in {college}.")
                    else:    
                        messages.info(request, f"Admin account for {designation} already exists in {college}.")

                else:
                    instance.designation = designation
                    instance.branch = branch
                    instance.user=request.user 
                    instance.save()
                    return redirect('admindashboard')
        else:
            form=AdminProfileForm()
    return render(request,'grievance/profileAdmin.html',{'form':form})

def previousComplaints(request):
    student=Student.objects.get(user=request.user)
    complains=Complain.objects.filter(sender=student)
    context={
        'complains':complains,
    }

    return render(request,'grievance/previousComplaints.html',context)

def studentComplainView(request,cid):
    complain=Complain.objects.get(id=cid)
    context={
        'complain':complain,
    }
    return render(request,'grievance/studentComplainView.html',context)

def adminComplainView(request,cid):
    complain = Complain.objects.get(id = cid)
    status = complain.status
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST, instance=complain)
        instance = form.save(commit=False)
        complain.status = instance.status
        complain.save()
        messages.info(request, f'Status changed successfully!')
        return redirect('admindashboard')
    else:
        form = ChangeStatusForm(instance=complain)
    return render(request, 'grievance/adminComplainView.html', {'form':form, 'complain':complain})

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

    }
    return render(request,'grievance/adminProfileView.html',context)

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
        s_form = EditStudent(request.POST, instance=student)
        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.info(request, 'Profile Updated Successfully!')
            return redirect('studentProfileView')
    else:
        u_form = EditUser(instance=user)
        s_form = EditStudent(instance=student)
    return render(request, 'grievance/student_editprofile.html', {'form1':u_form, 'form2':s_form})



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
    return render(request, 'grievance/admin_editprofile.html', {'form1':u_form, 'form2':a_form})  



def delete(request):
    user = request.user
    user.delete()
    messages.info(request, 'Account deleted successfully!')
    return redirect('home')


    
   