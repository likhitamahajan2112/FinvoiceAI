from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('balance/', views.balance_view, name='balance'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('api/input/', views.input_view, name='input'),
]