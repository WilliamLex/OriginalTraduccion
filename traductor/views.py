from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from gtts import gTTS
import os
from .models import Traduccion
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

from .forms import TaskForm

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
    
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def index(request):
    return render(request, 'index.html')


@login_required
def signout(request):
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
