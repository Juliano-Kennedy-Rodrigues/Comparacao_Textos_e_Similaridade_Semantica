from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def helloWorld(request):
    return HttpResponse('Hello World!')

def comparacao(request):
    return render(request, 'comparacao/index.html')

def yourName(request, name):
    return render(request, 'comparacao/yourname.html', {'name': name})

def dezArquivos(request):
    return render(request, 'comparacao/dezArquivos.html')

def cincoArquivos(request):
    return render(request, 'comparacao/cincoArquivos.html')