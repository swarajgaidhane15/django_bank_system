
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('phone_login/', include('phone_login.urls'),),
    path('', include('bank.urls')),
    path('api/', include('bank.api.urls')),
]
