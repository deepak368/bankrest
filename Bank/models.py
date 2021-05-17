from django.db import models


# Create your models here.
class Accounts(models.Model):
    account_num = models.IntegerField(unique=True)
    user_name = models.CharField(max_length=120, unique=True)
    balance = models.IntegerField(default=0)
    acnt_type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.account_num)


class Transactions(models.Model):
    accno=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    r_acno=models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now=True)
    def __str__(self):
         return str(self.accno)