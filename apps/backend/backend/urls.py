"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

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

See https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls edit admin page
"""

from django.contrib import admin
from django.urls import include, path

from .views import home

admin.site.site_header = "Restaurant Recommender Admin"
admin.site.site_title = "Restaurant Recommender Admin Portal"
admin.site.index_title = "Welcome to the Restaurant Recommender Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user_management.urls")),
    path("api/", include("restaurant_recommender.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", home, name="home"),
]
