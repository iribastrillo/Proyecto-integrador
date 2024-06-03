from django.urls import path

from . import views

urlpatterns = [
    path('', views.CoursesAndCareers.as_view(), name='careers'),  
    path('<pk>/detalle', views.DetailCareer.as_view(), name='detail-career'),
    path('<pk>/editar', views.UpdateCareer.as_view(), name='update-career'),
    path('<pk>/eliminar', views.DeleteCareer.as_view(), name='delete-career'),
    path('cursos/crear-curso/', views.CreateCourse.as_view(), name='create-course'),
    path('crear-carrera/', views.CreateCareer.as_view(), name='create-career'),
    path('<pk>/agregar-curso', views.AddCourseToCareer.as_view(), name='add-course'),
    path('cursos/', views.ListCourses.as_view(), name='courses'),
    path('cursos/<pk>/detalle', views.DetailCourse.as_view(), name='detail-course'),
    path('cursos/<pk>/editar', views.UpdateCourse.as_view(), name='update-course'),
    path('cursos/<pk>/eliminar', views.DeleteCourse.as_view(), name='delete-course'),

]