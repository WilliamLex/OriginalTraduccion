"""traducciones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from traductor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('traductor/', include('traductor.urls')),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('tarea/', views.tarea, name='tarea'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('tarea/<int:task_id>', views.task_detail, name='detalles_tarea'),
    path('taks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tarea/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('', include('traductor.urls'))
]
