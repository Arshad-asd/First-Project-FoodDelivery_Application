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
    path('contact',views.contact,name="contact"),
    path('contact_form_submit',views.contact_form_submit,name="contact_form_submit"),

    path('add_address',views.add_address,name="add_address"),
    path('edit_address',views.edit_address,name="edit_address"),
    path('delete_address',views.delete_address,name="delete_address"),
    path('profile',views.profile,name="profile"),
    path('update_photo',views.update_photo,name="update_photo"),
    path('menu_list',views.menu_list,name="menu_list"),
    path('specials',views.specials,name="specials"),
    path('category_products/<int:id>/',views.category_products,name="category_products"),
    path('item/<int:id>/',views.item,name="item"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('add_to_cart/', views.add_to_cart_nil, name="add_to_cart_nil"),
    path('update_cart_item/<int:id>/',views.update_cart_item,name="update_cart_item"),
    path('delete_cart_item/<int:id>',views.delete_cart_item,name="delete_cart_item"),
    path('cart',views.cart,name="cart"),

    path('user_coupons',views.user_coupons,name="user_coupons"),
    path('apply_coupon',views.apply_coupon,name="apply_coupon"),
    path('add_coupons',views.add_coupons,name="add_coupons"),
    path('coupon_list',views.coupon_list,name="coupon_list"),

    path('checkout',views.checkout,name="checkout"),
    path('order',views.order,name="order"),
    path('order_details',views.order_details,name="order_details"),
    path('cancelorderitem',views.cancelorderitem,name="cancelorderitem"),
    path('returnorderitem',views.returnorderitem,name="returnorderitem"),



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
    path('undo/<int:id>',views.undo,name="undo"),

    path('category',views.category,name="category"),
    path('category_list',views.category_list,name="category_list"),
    path('delete_category/<int:id>',views.delete_category,name="delete_category"),
    path('search_category',views.search_category,name="search_category"),

    path('orders',views.orders,name="orders"),
    path('change_order_status',views.change_order_status,name="change_order_status"),

    path('sales_report',views.sales_report,name="sales_report"),
    path('totalsales',views.totalsales,name="totalsales"),
    path('todaysales',views.todaysales,name="todaysales"),
    path('weeksales',views.weeksales,name="weeksales"),
    path('monthlysales',views.monthlysales,name="monthlysales"),
    path('yearlysales',views.yearlysales,name="yearlysales"),
    path('fromtosales',views.fromtosales,name="fromtosales"),

    path('users',views.users,name="users"),
    path('user_block/<int:id>',views.user_block,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblock,name="user_unblock"),

    path('razorpay_payment',views.razorpay_payment,name="razorpay_payment"),

]