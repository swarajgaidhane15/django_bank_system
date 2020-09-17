from django.urls import path
from . import views

app_name = 'bank'
urlpatterns = [
    path('', views.profile, name="profile"),
    path('update-profile/', views.update_profile, name="update_profile"),
    path('transactions/<int:pk>/', views.transactions, name="transactions"),
    path('<int:user_id>/create-trans/', views.add_trans, name="create_trans"),
    path('delete/<int:trans_id>/', views.delete_transaction, name="delete_trans"),
    path('login/', views.login_request, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout")
]