"""grouping_serv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings



urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("grouping_serv.apps.public.urls")),
    path("accounts/", include("grouping_serv.apps.accounts.urls")),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('logos/favicon.ico'))),
    path('i18n/', include('django.conf.urls.i18n')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
