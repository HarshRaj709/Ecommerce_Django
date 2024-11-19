from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-in/',views.usersignin,name='signin'),
    path('sign-up/',views.usersignup,name='signup'),
    path('logout/',views.userlogout,name='logout'),
    path('accounts/', include('allauth.urls')),

    #forgot password handling
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auths/password-reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auths/Email_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name='auths/new_cred.html'), name='password_reset_confirm'),
    #path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
