"""Bankrest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import UserRegisterMixin,AccountCreateView,Withdraw,Deposit,LoginView,LogoutView,Balance,TransactionSerializerView

urlpatterns = [
    path("register",UserRegisterMixin.as_view()),
    path("login",LoginView.as_view()),
    path("logout",LogoutView.as_view()),
    path("create",AccountCreateView.as_view()),
    path("balance/<int:accno>",Balance.as_view()),
    path("withdraw/<int:accno>",Withdraw.as_view()),
    path("deposit/<int:accno>",Deposit.as_view()),
    path("Transaction",TransactionSerializerView.as_view()),
    path("transaction/<int:accno>",TransactionSerializerView.as_view())
]