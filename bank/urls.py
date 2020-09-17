from django.urls import path
from . import views
from .views import TransactionsList

from django.contrib.auth.views import LoginView

app_name = 'bank'
urlpatterns = [
    path('', views.profile, name="profile"),
    path('update-profile/', views.update_profile, name="update_profile"),
    path('transactions/<int:pk>/', TransactionsList.as_view(), name="transactions"),
    path('<int:user_id>/create-trans/', views.add_trans, name="create_trans"),
    path('delete/<int:trans_id>/', views.delete_transaction, name="delete_trans"),
    path('login/', LoginView.as_view(template_name="bank/login.html"), name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout")
]
