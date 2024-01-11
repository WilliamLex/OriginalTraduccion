from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TipoTraduccion(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = 'TipoTraduccion'
        verbose_name_plural = 'TiposTraducciones'
        db_table = 'tipotraduccion'


class Traduccion(models.Model):
    texto = models.TextField()
    texto_traducido = models.TextField()
    tipo_traduccion = models.ForeignKey(TipoTraduccion, null=False, blank=False, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

     # Nuevo campo para la pronunciación en inglés
    pronunciacion = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self) -> str:
        return "{} | {}".format(self.texto, self.texto_traducido)

    class Meta:
        verbose_name = 'Traduccion'
        verbose_name_plural = 'Traducciones'
        db_table = 'traduccion'
    
class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username
