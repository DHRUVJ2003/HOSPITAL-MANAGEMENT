from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import routers

router = routers.SimpleRouter()
router.register('patients', views.Patients,basename='patients')
router.register('phmedicines',views.Phmedicines,basename='phmedicines')
router.register('patmedicines',views.patmedicines,basename='patmedicines')
router.register('patdiets',views.patdiets,basename='patdiets')
router.register('drdiets',views.drdiets,basename='drdiets')
router.register('drmedicines',views.drmedicines,basename='drmedicines')



urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.RegisterAPI.as_view(),name='register'),
    path('verify/<auth_token>',views.verification.as_view(),name='verify'),
    path('login/',views.LoginAPI.as_view(),name='login'),
    path('logout/',views.logoutt,name='logout'),
    path('oauth/', include('allauth.urls')),

    # re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    # path('api/authentication-test/', views.authentication_test),
    # path('addviewpatient/',views.PatientsLC.as_view(),name='addviewpatients')
]
# if settings.DEBUG:
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
                              
