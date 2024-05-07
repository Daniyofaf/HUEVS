from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('login/', views.account_login, name="account_login"),
    path('register/', views.account_register, name="account_register"),
    path('logout/', views.account_logout, name="account_logout"),
    path('reset-password/', views.auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', views.auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Other URL patterns...
    
]
