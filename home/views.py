from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as loginUser,logout
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import context
from .models import Profile,ForReset
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import uuid
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'index.html')

def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token_send.html')        

def register(request):
   
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
          
            try:
                if User.objects.filter(email = email).first():
                    messages.success(request,f'email is taken You are not able to log in')
                    return redirect('register')

                user_obj = User(username=username,email=email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                print(auth_token)
                profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
                profile_obj.save()
                #form.save()
                send_mail_after_register(email,auth_token)
                return redirect('token_send')
            except Exception as e:
                print(e)        
            #mail part
           

    else:
        form = CreateUserForm()
    return render(request,'register.html',{'form':form,'title':'reqister here'})           


def login(request):
    form = AuthenticationForm()
    context = {'form':form}
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password=password)
            user_obj = User.objects.filter(username = username).first()

            if user_obj is None:
                messages.success(request,f'user is not found')
                return redirect('login')

            profile_obj = Profile.objects.filter(user = user_obj).first() 

            if not profile_obj.is_varified:
                messages.success(request,f'profile is not varified check your mail')
                return redirect('login')    
            if user is not None: 
                loginUser(request,user)
                messages.success(request, f' wecome {username} !!')
                request.session['username'] = username
                return redirect('home')
            else:
                 messages.info(request, f'account done not exit plz sign in')

        else:
            messages.info(request, f'account done not exit plz sign in')
    return render(request, 'login.html',context)    

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_varified:
                messages.success(request, 'your account is already verified')
                return redirect('login')

            profile_obj.is_varified = True
            profile_obj.save()
            messages.success(request, 'your account has verified')
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)  
        return redirect('error')

def error_page(request):
    return render(request,'error.html')


def send_mail_after_register(email,token):
    subject = 'your account need to verifide'
    message = f'hi press the link to varify account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list) 

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        user = User.objects.filter(email = email).first()
        if user is not None:
            auth_token = str(uuid.uuid4())
            print(auth_token)
            profile_obj = ForReset(email = email, auth_token = auth_token)
            profile_obj.save()
            send_mail_for_reset(email,auth_token)
            return redirect('token_send')
            

    return render(request,'forget_password.html')
  
def send_mail_for_reset(email,token):
    subject = 'your account need to verifide'
    message = f'hi press the link to varify account http://127.0.0.1:8000/reset_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)   

def reset_verify(request, auth_token):
    try:
        profile_obj = ForReset.objects.filter(auth_token = auth_token).first()
        if profile_obj:           
            messages.success(request, 'your can reset your password here')
            return redirect('reset_password')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)  
        return redirect('/error')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            print(email ,password1,password2)
            password = make_password(password1)
            q = User.objects.filter(email = email).update(password = password)
            return redirect('login')
    return render(request,'reset_password.html')