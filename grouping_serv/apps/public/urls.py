from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "public"
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
