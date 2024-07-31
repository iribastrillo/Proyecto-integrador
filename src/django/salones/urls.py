from django.urls import path
from .views import (
    SalonesCreateView,
    SalonesListView,
    SalonesDetailView,
    SalonesUpdateView,
    SalonesDeleteView,
)


app_name = "salones"

urlpatterns = [
    path("", SalonesListView.as_view(), name="classrooms"),
    path("nuevo", SalonesCreateView.as_view(), name="create-classroom"),
    path("<int:pk>/detalle", SalonesDetailView.as_view(), name="detail-classroom"),
    path("<int:pk>/editar", SalonesUpdateView.as_view(), name="update-classroom"),
    path("<int:pk>/eliminar", SalonesDeleteView.as_view(), name="delete-classroom"),
]
