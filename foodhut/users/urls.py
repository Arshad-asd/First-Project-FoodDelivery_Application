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
    path('profileUpdate',views.profileUpdate,name="profileUpdate"),
    path('profile',views.profile,name="profile"),
    path('update_photo',views.update_photo,name="update_photo"),
    path('menu_list',views.menu_list,name="menu_list"),
    path('category_products/<int:id>/',views.category_products,name="category_products"),
    path('item/<int:id>/',views.item,name="item"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('add_to_cart/', views.add_to_cart_nil, name="add_to_cart_nil"),
    path('update_cart_item/<int:id>/',views.update_cart_item,name="update_cart_item"),
    path('delete_cart_item/<int:id>',views.delete_cart_item,name="delete_cart_item"),
    path('cart',views.cart,name="cart"),

    path('checkout',views.checkout,name="checkout"),



    path('signout',views.signout,name="signout"),
    path('enter_otp',views.enter_otp,name="enter_otp"),
    path('send_otp',views.send_otp,name="send_otp"),
    #admin side app paths
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('admin_signout',views.admin_signout,name="admin_signout"),
    path('search',views.search,name="search"),
    path('delete/<int:id>/',views.delete_data,name="delete_data"),
    path('/<int:id>/',views.user_edit,name="user_edit"),

    path('products',views.products,name="products"),
    path('add_product',views.add_product,name="add_product"),
    path('edit_product/<int:id>/',views.edit_product,name="edit_product"),
    path('delete_product/<int:id>',views.delete_product,name="delete_product"),

    path('category',views.category,name="category"),
    path('category_list',views.category_list,name="category_list"),
    path('delete_category/<int:id>',views.delete_category,name="delete_category"),
    path('search_category',views.search_category,name="search_category"),

    path('orders',views.orders,name="orders"),

    path('sales_report',views.sales_report,name="sales_report"),

    path('users',views.users,name="users"),
    path('user_block/<int:id>',views.user_block,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblock,name="user_unblock")

]