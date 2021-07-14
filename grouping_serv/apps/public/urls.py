from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView



app_name = "public"
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
