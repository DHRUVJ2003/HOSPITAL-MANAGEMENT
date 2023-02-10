from asyncio.windows_events import NULL
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import (AbstractUser)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.base_user import BaseUserManager

# from phonenumber_field.modelfields import PhoneNumberField
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        #email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

# Create your models here.
class USER(AbstractUser):
    username=None
    email = models.EmailField(primary_key=True)
    gender_choices=[('M','MALE'),('F','FEMALE'),('O','OTHERS')]
    # dept_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=1,choices=gender_choices)
    is_verified = models.BooleanField(default=False)

    # email=models.EmailField(max_length=254)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.email
class DEPARTMENT(models.Model):
    dept_name=models.CharField(max_length=50)

class DOCTORS(models.Model):
    doctor_id=models.ForeignKey(USER,on_delete=models.CASCADE)
    # deparment=models.ForeignKey(DEPARTMENTS,on_delete=models.CASCADE)
    # email=models.EmailField(max_length=254)
    dept_id=models.ForeignKey(DEPARTMENT,on_delete=models.CASCADE,default=NULL)
    contact_number=models.CharField(max_length=10)
    qualification=models.CharField(max_length=30)
    experience=models.IntegerField()
    # class Meta:
    #     permissions = [
    #         ("add_patients", "Can add patients"),
    #         ("change_patients", "Can change patients"),
    #         ("delete_patients", "Can delete patients"),
    #         ("view_patients", "Can view patients")
    #     ]

    def __str__(self):
        return str(self.doctor_id)

class PATIENTS(models.Model):
    patient_id=models.ForeignKey(USER,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DOCTORS,on_delete=models.CASCADE)
    # email=models.EmailField(max_length=254)
    # medicines=models.CharField(max_length=30)
    exercises=models.TextField()
    Previous_illnesses=models.TextField()
    age=models.IntegerField(default=0)

    def __str__(self):
        return str(self.patient_id)

class PHARMACISTS(models.Model):
    pharma_id=models.ForeignKey(USER,on_delete=models.CASCADE)
    # email=models.EmailField(max_length=254)
    experience=models.IntegerField()
    # class Meta:
    #     permissions = [
    #         ("view_patient", "Can view patients")
    #     ]
        
class PhMEDICINES(models.Model):
    medicine_name=models.CharField(max_length=30)
    quantity=models.IntegerField()
    cost=models.IntegerField()

class medicine(models.Model):
    patient=models.ForeignKey(PATIENTS,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DOCTORS,on_delete=models.CASCADE,default=NULL)
    medicine_name=models.CharField(max_length=30)
    duration=models.IntegerField()
    description=models.TextField()

class DIET(models.Model):
    patient=models.ForeignKey(PATIENTS,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DOCTORS,on_delete=models.CASCADE)
    food_name=models.CharField(max_length=30)
    quantity=models.CharField(max_length=30)
    meal_choices=[('B','BREAKFAST'),('L','LUNCH'),('D','DINNER')]
    meal_of_day=models.CharField(max_length=30,choices=meal_choices)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


    # reports=models.ImageField(upload_to='images/',default='images/xyz.jpg')
    