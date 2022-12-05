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



