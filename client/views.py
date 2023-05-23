from django.shortcuts import render
from events.models import Certificate

def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'my_certificates.html', {'certificates': certificates})

#to-do: criar a aba MY MARATHONS