from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from gtts import gTTS
import os
from .models import Traduccion

# Create your views here.


def index(request):
    return render(request, 'index.html')


def buscar_traduccion(_request, tipo_traduccion_id, texto_buscar):

    if tipo_traduccion_id == 3:
        traducciones = list(Traduccion.objects
                            .filter(texto__contains=texto_buscar)
                            .order_by('texto')
                            .prefetch_related('tipo_traduccion')
                            .values('texto', 'texto_traducido', 'tipo_traduccion__nombre'))
    else:
        traducciones = list(Traduccion.objects
                            .filter(texto__contains=texto_buscar)
                            .filter(tipo_traduccion__id=tipo_traduccion_id)
                            .order_by('texto')
                            .prefetch_related('tipo_traduccion')
                            .values('texto', 'texto_traducido', 'tipo_traduccion__nombre'))

    data = {
        'mensaje': "exito" if (len(traducciones) > 0) else "noencontradas",
        'traducciones': traducciones
    }
    return JsonResponse(data)
def obtener_pronunciacion(request):
    if request.method == 'POST':
        texto_traducido = request.POST.get('pronunciacion')

        # Usa gTTS para generar el archivo de audio
        tts = gTTS(text=texto_traducido, lang='en')
        audio_path = "pronunciacion.mp3"
        tts.save(audio_path)

        # Reproduce el audio utilizando pygame (si estás seguro de que pygame está instalado)
        os.system(f"start {audio_path}")

        # Verifica si el archivo de audio existe antes de intentar renderizar la plantilla
        if os.path.exists(audio_path):
            return render(request, 'traduccion.html', {'audio_path': audio_path})
        else:
            return HttpResponse("Error: No se pudo generar el archivo de audio.")
    else:
        return render(request, 'traduccion.html')
