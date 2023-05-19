from django.urls import path,include
from .import views

urlpatterns = [
    #user side app paths
    path('',views.welcome,name="welcome"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('forgot',views.forgot,name="forgot"),
    # path('reset',views.reset,name="reset"),
    path('home',views.home,name="home"),
    path('signout',views.signout,name="signout"),
    path('enter_otp',views.enter_otp,name="enter_otp"),
    path('send_otp',views.send_otp,name="send_otp"),
    #admin side app paths
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_panel',views.admin_panel,name="admin_panel"),
    path('admin_signout',views.admin_signout,name="admin_signout"),
    path('search',views.search,name="search"),
    path('delete/<int:id>/',views.delete_data,name="delete_data"),
    path('/<int:id>/',views.user_edit,name="user_edit"),

    path('admin_panel/products',views.products,name="products"),
    path('add_product',views.add_product,name="add_product"),
    path('users',views.users,name="users"),

]