from django.shortcuts import render
from requests import request
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serialisers import drdiet, phmedicines, register,patientserial,patmedicine,patdiet,drmedicine
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import PATIENTS, USER,DOCTORS, PhMEDICINES,medicine,DIET
from django.contrib.auth import authenticate,login,logout
from home import serialisers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from requests.exceptions import HTTPError

class RegisterAPI(APIView):
    def post(self, request,format=None):
        serializer = register(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("dhruv")        
        account= serializer.save()    
        user = serializer.data
        email = serializer.data['email']
        token = Token.objects.get(user=account).key
        send_mail_after_registration(email , token)
        return Response({'token': token,'user_data': user,'Success':'Your account is successfully created,please check your mail for verification'})
        # else:
        #     return Response(serializer.errors)

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = 'Hi click on the link to verify your account http://127.0.0.1:8000/verify/'+token
    print(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

class verification(APIView):
# @csrf_exempt 
    def get(self,request , auth_token):
        user_token= Token.objects.get(key = auth_token)
        user=USER.objects.get(email=user_token.user)
        print(user.is_verified)
        if user.is_verified:
            return Response({'verification done':'Your account is already verified.'})
        user.is_verified = True
        user.save()
        return Response({'verification done':'Your account has been verified.'})

class LoginAPI(APIView):	
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email = email, password = password)
        print(user)
        # serializer=LoginSerializer(user)
        # email = serializer.data['email']
        if user is not None :
            # login(request,user)
            userdet=USER.objects.get(email=user)
            if not userdet.is_verified:
                return Response({'login failed':'user is not verified'})
            login(request,user)
            print(user)
            token = Token.objects.get(user=user)
            return Response({'token' : token.key,'user' : user.email})
        return Response({'login failed':'Invalid Credentials'})

# @csrf_exempt 
# class LogoutAPI(APIView):
@csrf_exempt 
def logoutt(request):
    logout(request)
    return JsonResponse({'success': 'Sucessfully logged out'})

class Patients(PermissionRequiredMixin,viewsets.ModelViewSet):
    permission_required=()
    # permission_denied_message='access ddenied'
    serializer_class=patientserial
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        print(self.request.user)
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        print(doctor)
        return PATIENTS.objects.filter(doctor=doctor)
        # return PATIENTS.objects.all()

    def perform_create(self,serializer):
        # doctor=self.request.user
        # print(doctor)
        print(self.request.user)
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        serializer.save(doctor=doctor)
        print("success")
        return Response(serializer.data)

class Phmedicines(PermissionRequiredMixin,viewsets.ModelViewSet):
    permission_required=()
    queryset=PhMEDICINES.objects.all()
    serializer_class=phmedicines
    permission_classes=[permissions.IsAuthenticated]

class patmedicines(PermissionRequiredMixin,viewsets.ReadOnlyModelViewSet):
    permission_required=()
    serializer_class=patmedicine
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        patient=PATIENTS.objects.get(patient_id=self.request.user)
        return medicine.objects.filter(patient=patient)

class patdiets(PermissionRequiredMixin,viewsets.ReadOnlyModelViewSet):
    permission_required=()
    serializer_class=patdiet
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        patient=PATIENTS.objects.get(patient_id=self.request.user)
        return DIET.objects.filter(patient=patient)

class drdiets(PermissionRequiredMixin,viewsets.ModelViewSet):
    permission_required=()
    serializer_class=drdiet
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        return DIET.objects.filter(doctor=doctor)

    def perform_create(self,serializer):
        # doctor=self.request.user
        # print(doctor)
        print(self.request.user)
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        serializer.save(doctor=doctor)
        print("success")
        return Response(serializer.data)    

class drmedicines(PermissionRequiredMixin,viewsets.ModelViewSet):
    permission_required=()
    serializer_class=drmedicine
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        return medicine.objects.filter(doctor=doctor)

    def perform_create(self,serializer):
        # doctor=self.request.user
        # print(doctor)
        print(self.request.user)
        doctor=DOCTORS.objects.get(doctor_id=self.request.user)
        serializer.save(doctor=doctor)
        print("success")
        return Response(serializer.data)

# api_view(['POST'])
# @csrf_exempt 
# # @permission_classes([AllowAny])
# def register_by_access_token(request, backend):
#     token = request.POST['access_token']
#     print(token)
#     user = USER().save()
#     print(request)
#     if user:
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response(
#             {
#                 'token': token.key
#             },
#             status=status.HTTP_200_OK,
#             )
#     else:
#         return Response(
#             {
#                 'errors': {
#                     'token': 'Invalid token'
#                     }
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

# @csrf_exempt 
# @api_view(['GET', 'POST'])
# def authentication_test(request):
#     print(request.user)
