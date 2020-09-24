from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'bank'
urlpatterns = [
    path('', views.profile, name="profile"),
    path('users/', views.userlist, name="users"),
    path('update-profile/', views.update_profile, name="update_profile"),
    path('transactions/<int:pk>/', views.trasactionList, name="transactions"),
    path('<int:user_id>/create-trans/',
         views.AddTransaction.as_view(), name="create_trans"),
    path('delete/<int:trans_id>/', views.delete_transaction, name="delete_trans"),
    path('login/', auth_views.LoginView.as_view(template_name="bank/login.html"), name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='bank/users/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='bank/users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='bank/users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='bank/users/password_reset_complete.html'),
         name='password_reset_complete'),
]
