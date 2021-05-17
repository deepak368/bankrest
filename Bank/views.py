from rest_framework import generics
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status,mixins,permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Accounts,Transactions
from .serializer import UserModelSerializer, LoginSerializer, AccountModelSerializer, WithdrawSerializer,DepositSerializer,TransactionSerializer
from rest_framework.authtoken.models import Token

class UserRegisterMixin(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=UserModelSerializer
    def post(self,request):
        return self.create(request)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")
            # user=authenticate(request,username=username,password=password)
            user = User.objects.get(username=username)
            if (user.username==username)&(user.password==password):
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                return Response({"token":token.key},status=204)

class LogoutView(APIView):
    def get(self,request):
        logout(request)
        request.user.auth_token.delete()


class AccountCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountModelSerializer

    def get(self, request):
        acnt = Accounts.objects.last()
        if acnt:
            acno = acnt.account_num + 1
        else:
            acno = 1000
        return Response({"acno": acno})

    def post(self, request):
        return self.create(request)
class Balance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer=AccountModelSerializer
    def get(self,request,accno):
        accno=Accounts.objects.get(accno=accno)
        serializer=AccountModelSerializer(accno)
        return Response({"messege": "Balance is " + str(accno.balance)})

class Withdraw(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,accno):
        serializer=WithdrawSerializer(data=request.data)
        accno=Accounts.objects.get(accno=accno)
        if serializer.is_valid():
            amnt=serializer.validated_data.get("amount")
            if amnt<accno.balance:
                accno.balance-=amnt
                accno.save()
                return Response({"messege":"withdraw successfull , balance is "+str(accno.balance)})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Deposit(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,accno):
        serializer=DepositSerializer(data=request.data)
        accno=Accounts.objects.get(accno=accno)
        if serializer.is_valid():
            amnt=serializer.validated_data.get("amount")
            accno.balance+=amnt
            accno.save()
            return Response({"messege": "Deposit successfull , balance is " + str(accno.balance)})
            # return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TransactionSerializerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,accno):
        accno_obj=Accounts.objects.get(accno=accno)
        debit_transaction=Transactions.objects.filter(accno=accno_obj)
        print(debit_transaction)
        credit_transaction=Transactions.objects.filter(r_acno=accno)
        serializer1=TransactionSerializer(debit_transaction,many=True)
        serializer2=TransactionSerializer(credit_transaction,many=True)
        return Response({"All Debit Transactions ": serializer1.data ,"All  credit transaction":serializer2.data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            accno=serializer.validated_data.get("accno")
            r_acno=serializer.validated_data.get("r_acno")
            amount=serializer.validated_data.get("amount")
            accno_obj=Accounts.objects.get(accno=accno)
            r_acno_obj=Accounts.objects.get(accno=r_acno)
            if amount<=(accno_obj.balance):
                serializer.save()
                accno_obj.balance-=amount
                r_acno_obj.balance+=amount
                accno_obj.save()
                r_acno_obj.save()
                return Response({"msg ":str(amount) + " has been sent to acno: "+str(r_acno)})
            else:
                return Response({"No Sufficient balance"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)