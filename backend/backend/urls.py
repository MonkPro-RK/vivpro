"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import CustomLoginView,RegisterUser


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("songs.urls")),
    
    
    
        # Swagger Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    
    # User APIs
    path("api/register/", RegisterUser.as_view(), name="register"),
    path("api/login/", CustomLoginView.as_view(), name="custom_login"),

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
