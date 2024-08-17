"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy


from . import views

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(
            "accounts/login/",
            auth_views.LoginView.as_view(
                redirect_authenticated_user=True, next_page="home"
            ),
            name="login",
        ),
        path(
            "accounts/logout/",
            auth_views.LogoutView.as_view(next_page="login"),
            name="logout",
        ),
        path(
            "accounts/password-reset/",
            auth_views.PasswordResetView.as_view(),
            name="password_reset",
        ),
        path(
            "accounts/password-reset/done/",
            auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done",
        ),
        path(
            "accounts/reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        ),
        path(
            "accounts/reset/done/",
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        ),
        path(
            "accounts/password-change",
            views.CustomPasswordChangeView.as_view(),
            name="password-change",
        ),
        path("", RedirectView.as_view(url=reverse_lazy("home"))),
        path(
            "app/",
            include(
                [
                    path("", views.home, name="home"),
                    path("busqueda/", views.Search.as_view(), name="search"),
                    path("administracion/", views.dashboard, name="dashboard"),
                    path("carreras/", include("carreras.urls")),
                    path("profesores/", include("profesores.urls")),
                    path("salones/", include("salones.urls")),
                    path("clases/", include("clases.urls")),
                    path("perfil/", include("profiles.urls")),
                    path("estudiantes/", include("estudiantes.urls")),
                    path("pagos/", include("pagos.urls")),
                ]
            ),
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
