from ast import Pass
import imp
from lib2to3.pgen2 import token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Certificate
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
import csv
from secrets import token_urlsafe
import os
from django.conf import settings
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

@login_required
def new_marathon(request):
    if request.method == "GET":
        return render(request, 'new_marathon.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')

        main_color = request.POST.get('main_color')
        secondary_color = request.POST.get('secondary_color')
        bg_color = request.POST.get('bg_color')
        
        logo = request.FILES.get('logo')
        
        event = Event(
            creator=request.user,
            name=name,
            description=description,
            start_date=start_date,
            finish_date=finish_date,
            main_color=main_color,
            secondary_color=secondary_color,
            bg_color=bg_color,
            logo=logo,
        )
    
        event.save()

        messages.add_message(request, constants.SUCCESS, 'Marathon successfully registred')
        return redirect(reverse('new_marathon'))

@login_required      
def manage_marathon(request):
    if request.method == "GET":
        name = request.GET.get('name')
        events = Event.objects.filter(creator=request.user)
        #to-do: filtrar por outros tipos
        if name:
            events = events.filter(name__contains = name)

        return render(request, 'manage_marathon.html', {'events':events})

@login_required
def register_marathon(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "GET":
        return render (request, 'register_marathon.html', {'event': event})

    elif request.method == "POST":
        #to-do: validar se o usuário já é um participante
        event.users.add(request.user)
        event.save()

        messages.add_message(request, constants.SUCCESS, 'Cool! You are now registred in the marathon')

        return redirect(f'/events/register_marathon/{id}/')

def users_event(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('THIS MARATHON IS NOT YOURS')
    if request.method == "GET":
        users = event.users.all()
        return render(request, 'users_event.html', {'users': users, 'event': event})

def generate_csv(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('THIS MARATHON IS NOT YOURS')
    users = event.users.all()

    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for user in users:
            x = (user.username, user.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')
   
def certificate_event(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('THIS MARATHON IS NOT YOURS')
    if request.method == "GET":
        certificate_length = event.users.all().count() - Certificate.objects.filter(event=event).count()
        return render(request, 'certificate_event.html', {'certificate_length': certificate_length, 'event': event})

def generate_certificate(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('THIS MARATHON IS NOT YOURS')

    path_template = os.path.join(settings.BASE_DIR, 'templates/static/event/img/template_certificado.png')
    path_font = os.path.join(settings.BASE_DIR, 'templates/static/fonts/arimo.ttf')

    for user in event.users.all():
        #to-do validar se o certificado já foi gerado#
        img = Image.open(path_template)
        draw = ImageDraw.Draw(img)
        font_name = ImageFont.truetype(path_font, 80)
        font_info = ImageFont.truetype(path_font, 40)

        #to-do: arrumar o certificado
        draw.text((230, 651), f"{user.username}", font=font_name, fill=(0,0,0))
        draw.text((761, 782), f"{event.name}", font=font_info, fill=(0,0,0))
        draw.text((816, 849), f"{event.start_date} a {event.finish_date}", font=font_info, fill=(0,0,0))

        output = BytesIO()
        img.save(output, format="PNG", quality=100)
        output.seek(0)

        img_final = InMemoryUploadedFile(output, 'ImageField', f'{token_urlsafe(8)}.png', 'image/jpeg', sys.getsizeof(output), None)

        generated_certificate = Certificate(
            certificate=img_final,
            user=user,
            event=event
        )

        generated_certificate.save()

    messages.add_message(request, constants.SUCCESS, 'Certificates successfully generated!')
    return redirect(reverse('certificate_event', kwargs={'id': event.id}))  

def search_certificate(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('THIS MARATHON IS NOT YOURS')
    
    email = request.POST.get('email')
    certificate = Certificate.objects.filter(event=event).filter(user__email=email).first()

    if not certificate:
        messages.add_message(request, constants.ERROR, 'Certificate not generated yet!')
        return redirect(reverse('certificate_event', kwargs={'id': event.id}))

    return redirect(certificate.certificate.url) 