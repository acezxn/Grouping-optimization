from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"
urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("profile/send", views.submit_relation),
    path("profile/remove", views.remove_relation),
    path("signup", views.signup),
    path("list", views.list_user),
    path("compute", views.compute),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
