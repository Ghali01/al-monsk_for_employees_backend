from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):

    def create_user(self, email, firstName,secondName,password=None):
        user=User.objects.create(email=email,firstName=firstName,secondName=secondName)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email,password,firstName,secondName):
        user=self.create_user( email,firstName,secondName,password)        
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user
 
class User(AbstractBaseUser):
    is_active=models.BooleanField(default=True)
    last_login=models.DateTimeField(auto_now=True)  
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    email=models.EmailField(unique=True)
    firstName=models.CharField(max_length=40)
    secondName=models.CharField(max_length=40)
    online=models.BooleanField(default=False)
    EMAIL_FIELD='email'
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['firstName','secondName']

    objects=UserManager()

    
    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True


    def token(self): 
        return Token.objects.get(user=self)


class Employee(models.Model):
    start=models.TimeField()
    end=models.TimeField()
    user=models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name='employee')

class AttendRecord(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='attends')
    time=models.DateTimeField(auto_now_add=True)
    type=models.BooleanField()


class MACAdders(models.Model):
    address=models.CharField(max_length=20)
    name=models.CharField(max_length=50)
