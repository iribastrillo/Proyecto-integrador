from django.urls import path

from . import views

urlpatterns = [
    path("", views.CoursesAndCareers.as_view(), name="careers"),
    path("<slug:slug>/detalle", views.DetailCareer.as_view(), name="detail-career"),
    path("<slug:slug>/editar", views.UpdateCareer.as_view(), name="update-career"),
    path("<slug:slug>/eliminar", views.DeleteCareer.as_view(), name="delete-career"),
    path("cursos/crear", views.CreateCourse.as_view(), name="create-course"),
    path("crear/", views.CreateCareer.as_view(), name="create-career"),
    path("<pk>/agregar-curso", views.AddCourseToCareer.as_view(), name="add-course"),
    path("cursos/", views.ListCourses.as_view(), name="courses"),
    path(
        "cursos/<slug:slug>/detalle", views.DetailCourse.as_view(), name="detail-course"
    ),
    path(
        "cursos/<slug:slug>/editar", views.UpdateCourse.as_view(), name="update-course"
    ),
    path(
        "cursos/<slug:slug>/eliminar",
        views.DeleteCourse.as_view(),
        name="delete-course",
    ),
]
