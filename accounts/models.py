from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self,username,email,first_name,password=None):
        if not username:
            raise ValueError('Users must have an username.')
        if not email:
            raise ValueError('Users must have an email address.')
        email=self.normalize_email(email)
        user=self.model(username=username,email=email,first_name=first_name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,first_name,last_name,password=None):
        if not username:
            raise ValueError('Users must have an username.')
        if not email:
            raise ValueError('Users must have an email address.')
        email=self.normalize_email(email)
        user=self.model(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_staff=True
        user.save()
        return user
        

class UserAccount(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.EmailField(max_length=255,unique=True)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS=['email','first_name','last_name']
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        return self.first_name
    
    