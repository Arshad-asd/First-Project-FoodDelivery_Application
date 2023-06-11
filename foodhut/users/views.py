
from email import message
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.hashers import make_password
import os
# Create your views here.

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from twilio.rest import Client


from users.models import CustomUser,Category,Product,ProductSize,Cart, CartItem,ProfileAddress,ProfilePic

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
    request.session.flush()
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

def home(request):
    return render(request,"user/home.html")

def profile(request):
    user = request.user
    profile_address = ProfileAddress.objects.filter(user=user)
    profile_pic = ProfilePic.objects.get(user=user)
    if profile_address.exists():
        profile_address = profile_address.all()
    else:
        profile_address = None
    context = {
        'user': user,
        'profile_address': profile_address,
        'profile_pic':profile_pic,

    }
    return render(request, 'user/profile.html', context)

def profileUpdate(request):
    user = request.user
    if request.method == 'POST':
        print ('sdhgsvadhg')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')


        profile_address = ProfileAddress(user=user)
        profile_address.name=name
        profile_address.phone_number=mobile
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.postal_code = zip
        profile_address.save()
        return redirect('profile')
    
def update_photo(request):
    user = request.user
    try:
        profile_pic = ProfilePic.objects.get(user=user)
    except ProfilePic.DoesNotExist:
        # Handle the case when the user doesn't have a profile picture yet
        profile_pic=ProfilePic(user=user)
    
    if request.method == 'POST':
        new_profile_pic = request.FILES.get('profile_pic')
        if new_profile_pic:
            profile_pic.profile_pic = new_profile_pic
            print('photo undoo',new_profile_pic)
            profile_pic.save()
    return redirect('profile')



def menu_list(request):
    all_categories = Category.objects.all()
  
    return render(request,"user/menu_list.html",{"category":all_categories})

def category_products(request,id):
    all_categories = Category.objects.all()
    category = Category.objects.get(pk=id)
    products = Product.objects.filter(category=category)
    product_sizes = ProductSize.objects.all()
    return render(request,"user/menu_list.html", {'categorye': category, "category":all_categories, 'products': products})


def item(request,id):
    product = Product.objects.get(pk=id) 
    all_categories = Category.objects.all()
    return render(request,"user/item.html",{'product': product, "category":all_categories})


def add_to_cart_nil(request):
    print('sldkfjldskjfldfkjldsfj')
    return redirect('cart')

def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        cart, _ = Cart.objects.get_or_create(user=user)
        product_size_id = request.POST.get('product_size_id')  # Get the selected product size ID from the request

        # Check if the cart already contains the selected product and product size
        cart_item, created = cart.cart_items.get_or_create(product=product, product_size_id=product_size_id)

        if not created:
            cart_item.quantity += 1

        cart_item.save()

    return redirect('cart')

@require_POST
def update_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    new_quantity = int(request.POST.get('quantity', 0))
    if new_quantity >= 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect('cart')

def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    user = request.user if request.user.is_authenticated else None
    cart = Cart.objects.get(user=user) if user else None

    cart_items =CartItem.objects.filter(cart__user=user)

    context ={
        'cart':cart,
        'cart_items':cart_items
    }
    return render(request,'user/cart.html',context)

def checkout(request):
    # Get the current user
    user = request.user
    # Retrieve the user's cart
    cart = Cart.objects.get(user=user)
    # Retrieve the user's address
    address = ProfileAddress.objects.filter(user=user)

    context = {
        'addresses': address,
        'cart': cart,
    }

    return render(request, 'user/checkout.html', context)




def forgot(request):
    return render(request,"user/forgot.html")

#Email otp
# def send_otp(request):
#     error_message =None
#     otp = random.randint(11111,99999)
#     email = request.POST.get('email')
#     user_email = CustomUser.objects.filter(email=email)
#     if user_email:
#         user = CustomUser.objects.get(email = email)
#         user.otp =otp
#         user.save()
#         request.session['email'] = request.POST['email']
#         send_mail(
#             "welcome to foodhut",
#             "Your one time otp is"+str(otp),
#             "arshaarshad21@gmail.com",
#             [email],
#             fail_silently=False,
#         )
#         messages.success(request,'One time password send to yor email')
#         return redirect('enter_otp')
#     else:
#         error_message ="Invaild email please enter correct email"
#         return render(request,'user/forgot.html',{'error':error_message})

#-----------------------------------------Mobile_otp-Enter_otp-section------------------------------------------------------
# def enter_otp(request):
#     error_message =None
#     if request.session.has_key('email'):
#         email = request.session['email']
#         user = CustomUser.objects.filter(email=email)
#         for u in user:
#             user_otp = u.otp
#         if request.method=="POST":
#             otp =request.POST.get('otp')
#             if not otp:
#                 error_message= "otp is required"
#             elif not user_otp == otp:
#                 error_message ="otp is invalid"
#             if not error_message:
#                return redirect('home')
#         return render(request,'user/enter_otp.html')
#     else:
#         return render(request,"forgot.html")

def send_otp(request):
    mobile = request.POST.get('mobilenumber')
    user_number=CustomUser.objects.filter(mobile=mobile)
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)]) 
    if user_number.exists():
            user=user_number.first()
            user.otp=otp
            user.save()
            request.session['mobile']=mobile  # Replace with your OTP generation logic

    # Add your Twilio account credentials
            account_sid = 'AC2079bbb5b6cf31975f6788847cdca4b2'
            auth_token = '7cdd1b3e5f3014c588d93373a7e9e88a'
    # twilio_number = '+18306943453'

            client = Client(account_sid, auth_token)
            message = client.messages.create(
              body=' welcome to FOODHUT  Your OTP is: ' + otp,
              from_='+13614707012',
              to=mobile
            )
            return render(request,'user\enter_otp.html')
    else:
        messages.warning(request,"No user registered with the provided mobile number")
        return render(request, 'user/forgot.html')


def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        mobile = request.session.get('mobilenumber')

        user_number = CustomUser.objects.filter(mobile=mobile)
        if user_number.exists():
            user = user_number.first()
            if entered_otp == user.otp:
                # OTP verification successful
                user.is_otp_verified = True
                user.save()
                del request.session['mobilenumber']
                login(request, user)
                return redirect('home')
            else:
               messages.error(request, 'Invalid OTP')
               return render(request, 'user/enter_otp.html')

    return redirect('send_otp')  # Redirect to the O



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
        return redirect('admin_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user.is_superuser:
           login(request,user)
           return redirect('admin_home')
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
def admin_home(request):
    return render(request,"admin/admin_home.html")
#users list
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

#user block and unblock
def user_block(request,id):
    if request.method == 'POST':
         user = CustomUser.objects.get(pk=id)
         user.is_active =False
         user.save()
    return redirect('users')

def user_unblock(request,id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active=True
        user.save()
    return redirect('users')




#user edit option
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


#product management
def products(request):
    stu=Category.objects.all()
    products=Product.objects.all()
    product_sizes = ProductSize.objects.all()
    return render(request,'admin/products.html',{'products':products})


def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # Retrieve data from the form

        product_name = request.POST.get('productName')
        category_name=request.POST.get('category')
        Product_Image = request.FILES.get('image')
        category = Category.objects.get(categoryes=category_name)
        category_id = category.pk
        description = request.POST.get('description')
        sizes = [ 'medium', 'large','xl']
        print('product image:',Product_Image)
        if Product.objects.filter(Product_name=product_name):
            return render(request,'admin/add_product.html')
        else:
        # Create the product object
             product = Product(Product_name=product_name, category=category,description=description,Product_Image=Product_Image)
             product.save()
        # Create the product sizes and associate them with the product
        for size in sizes:
            checkbox = request.POST.get(f'checkbox-{size}')
            if checkbox:
                price = request.POST.get(f'price-{size}')
                # offer_price = request.POST.get(f'offer-price-{size}')
                quantity = request.POST.get(f'productCount-{size}')
                product_size = ProductSize(product_id=product, size=size, price=price,Quantity=quantity,)
                product_size.save()
    return render(request,"admin/add_product.html",{'categories':categories})


def edit_product(request,id):
    try:
        product = Product.objects.get(pk=id)
        sizes = product.productsize_set.all()
        category=Category.objects.all()
        context={
            'product':product,
            'sizes':sizes,
            'categories':category
        }
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    if request.method == 'POST':
        product_name = request.POST.get('productName')
        print(request.POST.get('categoryId'))
        category_id = request.POST.get('categoryId')
        category = get_object_or_404(Category, pk=category_id)        
        description = request.POST.get('description')
        if request.FILES.get('image'):
            photo = request.FILES.get('image')
        else:
            photo = product.Product_Image
        sizes = ['medium', 'large','xl']
        # Update the product details
        product.Product_name = product_name
        product.category  = category
        product.description = description
        product.Product_Image=photo
        product.save()
        
        for size in sizes:
            checkbox = request.POST.get(f'checkbox-{size}')
            if checkbox:
                price = request.POST.get(f'price-{size}')
                count = request.POST.get(f'productCount-{size}')
                    # Update or create the product size
                product_size, _ = ProductSize.objects.get_or_create(product_id=product, size=size)
                product_size.price = price
                product_size.Quantity = count
                product_size.save()


        return redirect('products')  # Redirect to a success page or product list view
    # If the request method is not POST, render the edit product form with the current product details
    return render(request,"admin/edit_product.html",context)


def delete_product(request,id):
    if request.method == 'POST':
        pi = Product.objects.get(pk=id)
        pi.delete()
        return redirect('products')



#category management
def category(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']
        if Category.objects.filter(categoryes=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/category.html', {'error_message': error_message})
        else:
            category = Category.objects.create(categoryes=category_name)
            stu=Category.objects.all()
            return render(request,'admin\category.html',{'stu':stu})  # Redirect to category list page

    return render(request,"admin/category.html")

def category_list(request):
    stu=Category.objects.all()
    return render(request,"admin/category.html",{'stu':stu})

def delete_category(request,id):
    if request.method=='POST':
        pi=Category.objects.get(pk=id)
        pi.delete()
        return redirect('category_list')

def search_category(request):
    if request.method == 'POST':
      query = request.POST['query']
      category = Category.objects.filter(Q(categoryes__icontains=query)|Q(id__contains=query))
    return render(request,"admin/search_category.html",{'category':category})

def orders(request):
    return render(request,"admin/orders.html")

def sales_report(request):
    return render(request,"admin/sales_report.html")