from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.serializers import ModelSerializer
from .models import Accounts,Transactions

class UserModelSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','username','password','email']

class AccountModelSerializer(ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_num', 'user_name', 'balance', 'acnt_type']
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class WithdrawSerializer(serializers.Serializer):
    amount=serializers.IntegerField()

class DepositSerializer(serializers.Serializer):
    amount=serializers.IntegerField()
class TransactionSerializer(serializers.Serializer):
    accno=serializers.CharField()
    r_acno=serializers.IntegerField()
    amount=serializers.IntegerField()
    date=serializers.DateField()
    def create(self, validated_data):
        accno=validated_data["accno"]
        account_obj=Accounts.objects.get(accno=accno)
        validated_data["accno"]=account_obj
        return Transactions.objects.create(**validated_data)
