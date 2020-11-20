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
    path("profile", views.classrooms),
    path("profile/<slug:q>/", views.ProfileView),
    path("rm/<slug:q>/", views.remove),
    path("create", views.create),
    path("join", views.join),
    path("dangerzone/<slug:q>/", views.dangerzone),
    path("edit/<slug:q>/", views.edit),
    path("signup", views.signup),
    path("list/<slug:q>/", views.list_user),
    path("compute/<slug:q>/", views.compute),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
