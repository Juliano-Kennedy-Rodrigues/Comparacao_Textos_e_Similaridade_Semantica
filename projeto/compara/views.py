from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def helloWorld(request):
    return HttpResponse('Hello World!')

def comparacao(request):
    return render(request, 'compara/index.html')

def yourName(request, name):
    return render(request, 'compara/yourname.html', {'name': name})