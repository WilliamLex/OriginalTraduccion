from django.urls import path
from .views import completed_tasks_report
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar_traduccion/<int:tipo_traduccion_id>/<texto_buscar>', views.buscar_traduccion, name='buscar_traduccion'),
    path('obtener_pronunciacion/', views.obtener_pronunciacion, name='obtener_pronunciacion'),
    path('completed_tasks_report/', completed_tasks_report, name='completed_tasks_report')
]

