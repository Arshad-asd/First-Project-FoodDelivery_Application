
from datetime import date, timedelta
from email import message
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.hashers import make_password
import os
from django.db.models import Sum
# Create your views here.

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect,JsonResponse
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from psycopg2 import IntegrityError
from twilio.rest import Client
from users.models import UserCoupon,ContactMessage,Wallet
from django.core.paginator import Paginator


from users.models import CustomUser,Category,Product,ProductSize,Cart, CartItem,ProfileAddress,ProfilePic,Order,OrderItems,Coupon

from.forms import Aforms
from django.db.models import Q

# Create your views here.

import razorpay
from foodhut.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET




def razorpay_payment(request):
    print(5555555555555555555555)
    user=request.user
    print(user.mobile,222222222222222222222222222222)
    if user is None:
         return render(request,'user/signup.html')
    
    cart = Cart.objects.get(user=user)
    payment_amount = cart.get_total()*100
    client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
    DATA = {
    "amount": float(payment_amount),
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    }
    order = client.order.create(data=DATA)
    print(8888888888888888888888888888888)
    res = {
        'success': True,
        'key_id': RAZOR_KEY_ID,
        'amount': float(payment_amount),
        'order_id': order['id'],
        'name': cart.user.name,
        'email': cart.user.email,
        'mobile': cart.user.mobile,
    }
    return JsonResponse(res)

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
@login_required(login_url='signin')
def profile(request):
    user = request.user
    
    profile_address = ProfileAddress.objects.filter(user=user)
    
    try:
        profile_pic = ProfilePic.objects.get(user=user)
    except ObjectDoesNotExist:
        profile_pic = None
    
    if profile_address.exists():
        profile_address = profile_address.all()
    else:
        profile_address = None
    
    context = { 
        'user': user,
        'profile_address': profile_address,
        'profile_pic': profile_pic,
    }
    
    return render(request, 'user/profile.html', context)


def add_address(request):
    user = request.user
    if request.method == 'POST':
        print ('sdhgsvadhg')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        house_no = request.POST.get('house_no')
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')


        profile_address = ProfileAddress(user=user)
        profile_address.name=name
        profile_address.phone_number=mobile
        profile_address.house_no=house_no
        profile_address.house_name=house_name
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.postal_code = zip
        profile_address.save()
        return redirect('profile')
    
def edit_address(request):
    user = request.user
    id = request.POST.get('address_id')
    print(id,'id kittyo')
    profile_address = ProfileAddress.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        house_no = request.POST.get('house_no')
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')

        profile_address.name = name
        profile_address.phone_number = mobile
        profile_address.house_no = house_no
        profile_address.house_name = house_name
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.postal_code = zip
        profile_address.save()
        return redirect('profile')
    return render(request, 'user/profile.html')

@require_POST
def delete_address(request):
    user = request.user
    address_id = request.POST.get('address_id')

    if address_id:
        try:
            address_id = int(address_id)
            profile_address = get_object_or_404(ProfileAddress, id=address_id, user=user)
            profile_address.delete()
        except (ValueError, ProfileAddress.DoesNotExist):
            pass

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
    products = Product.objects.filter(is_deleted=False)  # Query the Product model for the products
    paginator = Paginator(products, per_page=4)  # Display 4 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_categories = Category.objects.all()
    context = {
        "category": all_categories,
        "page_obj": page_obj,
        "products": products
    }
    return render(request, "user/menu_list.html", context)

def specials(request):
    products = Product.objects.filter(is_deleted=False)  # Query the Product model for the products
    paginator = Paginator(products, per_page=4)  # Display 4 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_categories = Category.objects.all()
    context = {
        "category": all_categories,
        "page_obj": page_obj,
        "products": products
    }
    return render(request,"user/specials.html",context)
def category_products(request,id):
    all_categories = Category.objects.all()
    category = Category.objects.get(pk=id)
    products = Product.objects.filter(category=category,is_deleted=False)
    print(products,111111111111111111111111111)
    product_sizes = ProductSize.objects.all()  
    paginator = Paginator(products, per_page=4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context={
               'categorye': category,
               "category":all_categories, 
               "page_obj": page_obj,
               'products': products
    }
    return render(request,"user/menu_list.html",context)


def item(request,id):
    product = Product.objects.get(pk=id) 
    all_categories = Category.objects.all()
    context = {
              'product': product, 
              "category":all_categories,
    }
   
    return render(request,"user/item.html",context)


def add_to_cart_nil(request):
    print('sldkfjldskjfldfkjldsfj')
    return redirect('cart')

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Product, Cart

def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        cart, _ = Cart.objects.get_or_create(user=user)
        product_size_id = request.POST.get('product_size_id')  # Get the selected product size ID from the request

        if product_size_id is not None:
            try:
                # Check if the cart already contains the selected product and product size
                cart_item, created = cart.cart_items.get_or_create(product=product, product_size_id=product_size_id)

                if not created:
                    cart_item.quantity += 1
                    if cart_item.quantity > cart_item.product_size.Quantity:
                        cart_item.quantity = cart_item.product_size.Quantity
                cart_item.save()

            except IntegrityError:
                messages.error(request, 'Please select a valid size.')
                
        else:
            messages.error(request, 'Please select a size.')
            return redirect('item',id)

    return redirect('cart')



@require_POST
# def update_cart_item(request, id):
#     cart_item = get_object_or_404(CartItem, id=id)
#     new_quantity = int(request.POST.get('quantity', 0))

#     # Retrieve the available stock for the product size
#     available_stock = cart_item.product_size.Quantity

#     if new_quantity >= 0 and new_quantity <= available_stock:
#         cart_item.quantity = new_quantity
#         cart_item.save()
#     else:
#         error_message = f"Invalid quantity. Please enter a value between 0 and {available_stock}."
#         messages.error(request, error_message)
#     return redirect('cart')

def update_cart_item(request, id):
    user=request.user
    cart_item = get_object_or_404(CartItem, id=id)
    cart=Cart.objects.get(user=user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 0))
        if new_quantity >= 0:
            cart_item.quantity = new_quantity
            cart_item.save()

    # Prepare the data to be sent back in the AJAX response
    data = {
        'subtotal': cart_item.get_subtotal(),
        'price':cart.get_total_price(),
        'quantity':cart.get_total_quantity(),
    }
        # Return the updated data as a JSON response
    return JsonResponse(data)

def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    user = request.user if request.user.is_authenticated else None
    
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        context = {
            'cart': cart,
            'cart_items': cart_items
        }
        return render(request, 'user/cart.html', context)
    except ObjectDoesNotExist:
        return render(request, 'user/empty_cart.html')

def user_coupons(request):
    coupons = Coupon.objects.all()
    context ={
        'coupons':coupons,
    }
    return render(request,"user/user_coupons.html",context)

def coupon_list(request):
    categories = Category.objects.all()
    coupons = Coupon.objects.all()
    context ={
        'categories':categories,
        'coupons':coupons,
    }
    return render(request,"admin/coupons.html",context)


def add_coupons(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        active = bool(request.POST.get('active'))
        applicable_type = request.POST.get('category')
        category = request.POST.get('categorySelection')

        discount_type = request.POST.get('discount_type')
        discount = request.POST.get('discount')

        coupon = Coupon(
            code=code,
            name=name,
            description=description,
            discount_type=discount_type,
            discount=discount,
            start_date=start_date,
            end_date=end_date,
            active=active,
            applicable_type=applicable_type,
            category=category,
        )
        coupon.save()
        return redirect('coupon_list')

    return render(request, 'admin/coupons.html')


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')
        user = request.user
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.warning(request, "COUPON CODE DOES NOT EXIST")
            return redirect('cart')
        
        if not coupon.is_valid():
            messages.warning(request, "COUPON CODE IS NOT VALID")
            return redirect('cart')

        if UserCoupon.objects.filter(user=user, coupon_applied=coupon).exists():
            messages.warning(request, "YOU HAVE ALREADY USED THIS COUPON")
            return redirect('cart')

        cart, _ = Cart.objects.get_or_create(user=user)  
        if cart.get_total() < coupon.min_amount:
            messages.warning(request, "MINIMUM CART AMOUNT NOT MET")
            return redirect('cart')
  
        applicable_type = coupon.applicable_type
        if applicable_type == 'Category All':
            # Apply coupon to all categories
            cart.coupon_applied = coupon
            cart.save()
            UserCoupon.objects.create(user=user, coupon_applied=coupon)
            messages.success(request, "COUPON APPLIED SUCCESSFULLY")
            return redirect('cart')
        elif applicable_type == 'Category':
            category = coupon.category
            if CartItem.objects.filter(cart=cart, product__category=category).exists():
                    cart.coupon_applied = coupon
                    cart.save()
                    UserCoupon.objects.create(user=user, coupon_applied=coupon)
                    messages.success(request, "COUPON APPLIED SUCCESSFULLY")
                    return redirect('cart')
            else:
                    messages.warning(request, "COUPON IS NOT APPLICABLE TO SELECTED CATEGORY")
                    return redirect('cart')
        else:
            messages.warning(request, "INVALID APPLICABLE TYPE")
            return redirect('cart')
    return redirect('cart')

def checkout(request):
    # Get the current user
    user = request.user
    # Retrieve the user's cart
    cart = Cart.objects.get(user=user)
    # Retrieve the user's address
    cart_items = CartItem.objects.filter(cart__user=user)
    address = ProfileAddress.objects.filter(user=user)
    balance = Wallet.objects.get(user=user)

    context = {
        'addresses': address,
        'cart': cart,
        'cart_items':cart_items,
        'balance':balance,
    }

    return render(request, 'user/checkout.html', context)


def order(request):
    user=request.user
    address_id = request.POST.get('idpassed')
    payment_method = request.POST.get('payment_modal2')
    wallet=request.POST.get('wallet_modal')
    if not address_id:
            messages.error(request, 'Please select an address.')
            return redirect('checkout')
    if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('checkout')
    address = ProfileAddress.objects.get(pk=address_id)
    cart_items =CartItem.objects.filter(cart__user=user)
    cart = Cart.objects.get(user=user)
    total_mrp = cart.get_total_price()  
    discount_price = cart.get_total_discount()
    coupon_discount = 0
    delivery_charge = cart.get_shipping_charge() 
    payment_amount = cart.get_total()
    order_status = "Pending"
    balance=Wallet.objects.get(user=user)
    if payment_method =="razorpay":
        order.order_status = 'Paid'
        order.payment_status = 'Completed'
        order.save()
    if wallet=='true':
        if balance.balance > cart.get_total():
            payment_amount=0
            balance.balance=balance.balance-cart.get_total()
            balance.save()
        else:
            payment_amount=cart.get_total()-balance.balance
            balance.balance=0
            balance.save()
        # Create a new order instance
    order = Order(
            user=request.user,
            order_status='Pending',
            payment_status='Pending',
            payment_method=payment_method,
            checkout_status='Completed',
            to_address=address,
            total_mrp=total_mrp,
            discount_price=discount_price,
            coupon_discount=coupon_discount,
            delivery_charge=delivery_charge,
            payment_amount=payment_amount
        )
    order.save()
    for cart_item in cart_items:
                order_item = OrderItems(
                    order_no=order,
                    product=cart_item.product,
                    order_status=order_status,
                    product_size=cart_item.product_size,
                    quantity=cart_item.quantity,
                    amount=cart_item.get_subtotal()
                )
                order_item.save()
                product = cart_item.product
                product_size = ProductSize.objects.get(product_id=product, size=cart_item.product_size.size)
                product_size.Quantity -= cart_item.quantity
                product_size.save()
    cart.delete()
    return render(request,'user/codsuccess.html')




def order_details(request):#user side
      user=request.user
      order=Order.objects.filter(user=user)
      order_items=OrderItems.objects.filter(order_no__in=order)
      contex={
      'user':user,     
      'order':order,
      'order_items':order_items,
      }
      return render(request,'user/order_details.html',contex)


def cancelorderitem(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('itemId'))
        print(type(item_id),'0000000000000000000')
        order_item = OrderItems.objects.get(id=item_id)
        if order_item:
            order_item.order_status = 'Canceled'
            order_item.save()
            product_size = order_item.product_size
            product_size.Quantity += order_item.quantity
            product_size.save()
            return JsonResponse({'message': 'Item canceled successfully'})
        else:
            return JsonResponse({'error': 'Item not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def returnorderitem(request):
    if request.method == 'POST':
        id = request.POST.get('itemid')
        print(id,'000000000000000000000000000000000000000')
        order_id = request.POST.get('order_id')
        print(order_id,'9999999999999999999999999')
        return_reasons = {
            'defective': 'Defective or damaged product',
            'poor_quality': 'Poor quality or not as described',
            'wrong_item': 'Item is not what I ordered',
            'dislike': 'Don\'t like the product',
        }
        return_reason = request.POST.get('return_reason')
        other_reason = return_reasons.get(return_reason, '')
        if return_reason == 'other':
            other_reason = request.POST.get('other_reason', '')
        
        order_item = OrderItems.objects.get(id=id)
        print()
        if order_item is not None:
            order_item.order_status = 'Returned'
            order_item.return_problem = other_reason
            order_item.save()
            
            order = Order.objects.get(order_id=order_id)
            has_active_items = OrderItems.objects.filter(order_no=order_id).exclude(order_status=['Returned', 'Cancelled']).exists()
            if not has_active_items:
                order.order_status = 'Returned'
                order.save()
            print('saved88888888888888888888888888')
            return redirect('order_details')
        else:
            return HttpResponse("Item not found.")
    
    return HttpResponse("Invalid request.")

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

def contact(request):
    subject_choices = ContactMessage.SUBJECT_CHOICES
    context = {
        'subject_choices': subject_choices
    }
    return render(request,"user/contact.html",context)


def contact_form_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a new ContactMessage instance and save the form data
        contact_message = ContactMessage()
        contact_message.name = name
        contact_message.email = email
        contact_message.subject = subject
        contact_message.message = message
        contact_message.user = request.user  # Assign the current user
        contact_message.save()
        
        messages.success(request, 'Message sent successfully!')
    
    return render(request, 'contact.html')

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
    # Get the count of each order status
    delivered_count = OrderItems.objects.filter(order_status='Delivered').count()
    pending_count = OrderItems.objects.filter(order_status='Pending').count()
    shipping_count = OrderItems.objects.filter(order_status='Out for Shipping').count()
    cancel_count = OrderItems.objects.filter(order_status='Canceled').count()
    returned_count = OrderItems.objects.filter(order_status='Returned').count()

    # Pass the values to the template context
    context = {
        'delivered_count': delivered_count,
        'pending_count': pending_count,
        'shipping_count': shipping_count,
        'cancel_count': cancel_count,
        'returned_count': returned_count,
    }

    return render(request,"admin/chart.html",context)
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
                offer_price = request.POST.get(f'offer-price-{size}')
                quantity = request.POST.get(f'productCount-{size}')
                product_size = ProductSize(product_id=product, size=size, price=price,offer_price=offer_price,Quantity=quantity,)
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
                offer_price = request.POST.get(f'offer-price-{size}')
                count = request.POST.get(f'productCount-{size}')
                    # Update or create the product size
                product_size, _ = ProductSize.objects.get_or_create(product_id=product, size=size)
                product_size.price = price
                product_size.offer_price =offer_price
                product_size.Quantity = count
                product_size.save()


        return redirect('products')  # Redirect to a success page or product list view
    # If the request method is not POST, render the edit product form with the current product details
    return render(request,"admin/edit_product.html",context)


# def delete_product(request,id):
#     if request.method == 'POST':
#         pi = Product.objects.get(pk=id)
#         pi.delete()
#         return redirect('products')

def delete_product(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.soft_delete()
        return redirect('products')
def undo(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.is_deleted = False
        product.save()
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
    stu=CustomUser.objects.all()
    order=Order.objects.all()
    order_items = OrderItems.objects.all()
    order_status_choices = OrderItems.ORDER_STATUS
    context={
         'orders':order,
         'order_items':order_items,
         'choices':order_status_choices
    }
    
    return render(request,"admin/orders.html",context)

def change_order_status(request):
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        print(order_item_id,'11111111111111111111111111111111111111111111')
        new_status = request.POST.get('order_status')
        print(new_status,'88888888888')
        try:
            order_item = OrderItems.objects.get(id=order_item_id)
            order_item.order_status = new_status
            order_item.save()
        except OrderItems.DoesNotExist:
            pass
        return redirect('orders')  # Redirect to a suitable page after changing the status
    return render(request, 'admin/order.html')

def sales_report(request):
    return render(request,"admin/sales_report.html")

def totalsales(request):
    today = date.today()
    order_items = OrderItems.objects.all()
    total_payment_amount = Order.objects.filter(order_date__date__lte=today).aggregate(total=Sum('payment_amount'))
    orders = Order.objects.filter(order_date__date__lte=today)
    total_amount = total_payment_amount['total'] if total_payment_amount['total'] else 0
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'orderitems':order_items
    }
    return render(request,'admin/sales_report.html',context)

def todaysales(request):
    today = date.today()
    total_payment_amount = Order.objects.filter(order_date__date=today).aggregate(total=Sum('payment_amount'))
    orders = Order.objects.filter(order_date__date=today)
    total_amount = total_payment_amount['total'] if total_payment_amount['total'] else 0
    context= {
        'total_payment_amount': total_amount,
        'orders': orders
    }
    return render(request,'admin/sales_report.html',context)
def weeksales(request):
    today = date.today()
    start_date = today - timedelta(days=6)  # Get the start date (today - 6 days)
    end_date = today
    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders
    }
    return render(request,'admin/sales_report.html',context)
def monthlysales(request):
    today = date.today()
    start_date = today.replace(day=1)  # Get the first day of the current month
    end_date = today
    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders
    }
    return render(request,'admin/sales_report.html',context)

def yearlysales(request):
    today = date.today()
    start_date = today.replace(month=1, day=1)  
    end_date = today.replace(month=12, day=31)
    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders
    }
    return render(request,'admin/sales_report.html',context)
def fromtosales(request):
    if request.method == 'POST':
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
    orders = Order.objects.filter(order_date__range=[from_date, to_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders
    }
    return render(request,'admin/sales_report.html',context)
