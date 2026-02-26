from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('apply/', views.apply_loan, name='apply_loan'),
    path('loan/<int:pk>/', views.loan_detail, name='loan_detail'),
    path('loan/<int:pk>/pay/', views.make_payment, name='make_payment'),
    path('loan/<int:pk>/approve/', views.approve_loan, name='approve_loan'),
    path('loan/<int:pk>/reject/', views.reject_loan, name='reject_loan'),
]
