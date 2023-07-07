from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Category, Product, ProductSize,Cart,CartItem,ProfileAddress,ProfilePic,Order,OrderItems,Coupon
from users.models import CustomUser,UserCoupon,ContactMessage,Wallet
# Register your models here.
class CustomUser(admin.ModelAdmin):
    list_display = ('name','email', 'password','mobile')
admin.site.register(get_user_model())
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProfileAddress)
admin.site.register(ProfilePic)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Coupon)
admin.site.register(UserCoupon)
admin.site.register(ContactMessage)
admin.site.register(Wallet)
