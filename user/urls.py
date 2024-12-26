from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('accounts/google/callback/', views.google_callback, name='google_callback'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('seller/signup/', views.seller_signup, name='seller_signup'),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/logout/', views.seller_logout, name='seller_logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('my_cart/', views.my_cart, name='my_cart'),

]