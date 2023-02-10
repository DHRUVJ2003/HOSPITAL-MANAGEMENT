from django.contrib import admin
from .models import DEPARTMENT, USER,DOCTORS,PATIENTS,PHARMACISTS,PhMEDICINES,medicine,DIET

# Register your models here.
@admin.register(USER)
class userAdmin(admin.ModelAdmin):
    fields=['email','password','first_name','last_name','gender','is_superuser','is_verified']
    list_display = ['email','password','first_name','last_name','gender','is_superuser','is_verified']

@admin.register(DOCTORS)
class userAdmin(admin.ModelAdmin):
    fields=['doctor_id','contact_number','qualification','experience','dept_id']
    list_display = ['id','doctor_id','contact_number','qualification','experience','dept_id']

@admin.register(PATIENTS)
class userAdmin(admin.ModelAdmin):
    # readonly_fields = ('id')
    fields=['patient_id','doctor','exercises','Previous_illnesses','age']
    list_display = ['id','patient_id','doctor','exercises','Previous_illnesses','age']

@admin.register(PHARMACISTS)
class userAdmin(admin.ModelAdmin):
    fields=['pharma_id','experience']
    list_display = ['id','pharma_id','experience']

@admin.register(PhMEDICINES)
class userAdmin(admin.ModelAdmin):
    fields=['medicine_name','quantity','cost']
    list_display = ['id','medicine_name','quantity','cost']

@admin.register(medicine)
class userAdmin(admin.ModelAdmin):
    fields=['patient','doctor','medicine_name','duration','description']
    list_display = ['id','patient','doctor','medicine_name','duration','description']

@admin.register(DEPARTMENT)
class userAdmin(admin.ModelAdmin):
    fields=['dept_name']
    list_display = ['id','dept_name']

@admin.register(DIET)
class userAdmin(admin.ModelAdmin):
    fields=['patient','doctor','food_name','quantity','meal_of_day']
    list_display = ['id','patient','doctor','food_name','quantity','meal_of_day']

from django.contrib.auth.models import Permission
admin.site.register(Permission)
