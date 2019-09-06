from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Books
from .forms import AuthorForm
# Create your views here.

#def index(request):
#	return render(request,forms.Author,'downloads/landing.html')

#def download(request):
#	return render(request,'downloads/index.html',{'obj':Books.objects.values('Author').distinct()})