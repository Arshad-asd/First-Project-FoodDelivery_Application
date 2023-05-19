
from email import message
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.hashers import make_password
# Create your views here.

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from users.models import CustomUser
from.forms import Aforms
from django.db.models import Q

# Create your views here.

#USER SIDE
def welcome(request):

    return render(request,"user/welcome.html")
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        Phonenumber = request.POST['Phonenumber']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if CustomUser.objects.filter(name=name):
            messages.error(request,"Email already Registered!!")
            return redirect('signup')

        if pass1 == pass2:
            myuser = CustomUser.objects.create_user(name=name,email=email,mobile =Phonenumber,password=pass1)
            myuser.save()
            return redirect("signin")
        else:
            messages.error(request,"your password and confirm password incorrect")
            return redirect("signup")


    return render(request,"user/signup.html")
@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email= email,password=password)
        if user is not None:
           login(request,user)
           return redirect("home")
        else:
            messages.error(request,"User name or password is incorect")

    return render(request,"user/login.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

@never_cache
@login_required(login_url='signin')
def home(request):
    return render(request,"user/home.html")

def forgot(request):
    return render(request,"user/forgot.html")

def send_otp(request):
    error_message =None
    otp = random.randint(11111,99999)
    email = request.POST.get('email')
    user_email = CustomUser.objects.filter(email=email)
    if user_email:
        user = CustomUser.objects.get(email = email)
        user.otp =otp
        user.save()
        request.session['email'] = request.POST['email']
        send_mail(
            "welcome to foodhut",
            "Your one time otp is"+str(otp),
            "arshaarshad21@gmail.com",
            [email],
            fail_silently=False,
        )
        messages.success(request,'One time password send to yor email.')
        return redirect('enter_otp')
    else:
        error_message ="Invaild email please enter correct email"
        return render(request,'user/forgot.html',{'error':error_message})
def enter_otp(request):
    error_message =None
    if request.session.has_key('email'):
        email = request.session['email']
        user = CustomUser.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method=="POST":
            otp =request.POST.get('otp')
            if not otp:
                error_message= "otp is required"
            elif not user_otp == otp:
                error_message ="otp is invalid"
            if not error_message:
               return redirect('home')
        return render(request,'user/enter_otp.html')
    else:
        return render(request,"forgot.html")


# def reset(request):
#     error_message = None
#     if request.session.has_key('email'):
#         email = request.session['email']
#         user = CustomUser.objects.get(email=email)
#         if request.method =="POST":
#             newpassword =request.POST.get('new_password')
#             confirmpassword = request.POST.get('confirmpassword')
#             if newpassword:
#                 error_message= "enter new password"
#             elif not confirmpassword:
#                 error_message ="enter new confirm passworde"
#             elif newpassword == user.password:
#                 error_message = "this password already exist"
#             if not error_message:
#                 user.set_password(newpassword)
#                 print(user.password)
#                 user.save() 
                
#                 messages.success(request,"password changed Sucess fully")
#                 return redirect('signin')
#     return render(request,"user/reset.html",{'error':error_message})



#ADMIN SIDE

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user.is_superuser:
           login(request,user)
           return redirect('admin_panel')
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')

    return render(request,"admin/admin_login.html")

def admin_signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_login')



@never_cache
@login_required(login_url='admin_login')
def admin_panel(request):
    return render(request,"admin/admin_panel.html")

def users(request):
    if request.method == "POST":
        fm = Aforms(request.POST)
        if fm.is_valid():
            fm.save()
        fm = Aforms()
    else:
        fm = Aforms()
    stu =CustomUser.objects.all()
    return render(request,"admin/users.html",{'fm':fm,'stu':stu})

def user_edit(request,id):
    if request.method =='POST':
        pi = CustomUser.objects.get(pk=id)
        fm =Aforms(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
            pi = CustomUser.objects.get(pk=id)
            fm =Aforms(instance=pi)
    return render(request,"admin/user_edit.html",{'form':fm})

#this function delete user
def delete_data(request,id):
    if request.method == 'POST':
        pi = CustomUser.objects.get(pk=id)
        pi.delete()
        return redirect('users')

#search a user

def search(request):
    if request.method == 'POST':
      query = request.POST['query']
      user = CustomUser.objects.filter(Q(name__icontains=query)|Q(email__icontains=query)|Q(id__contains=query))
    return render(request,"admin/search.html",{'user':user})

def products(request):
    return render(request,"admin/products.html")

def add_product(request):
    return render(request,"admin/add_product.html")
