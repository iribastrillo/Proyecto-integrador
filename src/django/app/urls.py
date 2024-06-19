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
from django.conf.urls.static import static
from django.urls import path, include


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
            "accounts/password-change",
            views.CustomPasswordChangeView.as_view(),
            name="password-change",
        ),
        path(
            "app/",
            include(
                [
                    path("", views.dashboard, name="home"),
                    path("carreras/", include("carreras.urls")),
                    path("profesores/", include("profesores.urls")),
                    path("salones/", include("salones.urls")),
                    path("clases/", include("clases.urls")),
                    path("perfil/", include("profiles.urls")),
                    path("estudiantes/", include("estudiantes.urls")),
                ]
            ),
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
