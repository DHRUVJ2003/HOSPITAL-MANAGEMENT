from rest_framework import serializers
from .models import PATIENTS, USER,PhMEDICINES,medicine,DIET

class register(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = USER
        fields = ['email','password','password2','first_name', 'last_name','gender']
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True},'first_name':{'required':True},'last_name':{'required':True}}
        

    def create(self, validated_data):
        user = USER(
            # username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],

            # password=validated_data['password'],
            # password2=validated_data['password2'],
        )
        password=validated_data['password'],
        password2=validated_data['password2'],
        if (password==password2):
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = USER
#         fields = ['email','password']
class patientserial(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source='patient.doctor')
    class Meta:
        model=PATIENTS
        fields=['patient_id','doctor','exercises','Previous_illnesses','age']

class phmedicines(serializers.ModelSerializer):
    class Meta:
        model=PhMEDICINES
        fields=['medicine_name','quantity','cost']

class patmedicine(serializers.ModelSerializer):
    patient = serializers.ReadOnlyField(source='medicine.patient')
    class Meta:
        model=medicine
        fields=['patient','medicine_name','description','duration']

class patdiet(serializers.ModelSerializer):
    patient = serializers.ReadOnlyField(source='DIET.patient')
    class Meta:
        model=DIET
        fields=['patient','food_name','quantity','meal_of_day']

class drdiet(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source='DIET.doctor')
    class Meta:
        model=DIET
        fields=['doctor','patient','food_name','quantity','meal_of_day']

class drmedicine(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source='medicine.doctor')
    class Meta:
        model=medicine
        fields=['doctor','patient','medicine_name','description','duration']