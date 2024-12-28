from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('search_results/', views.search_results, name='search_results')

] 