from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Books
from .forms import AuthorForm
from django.db.models import Count
from django.forms import ModelForm
from django.urls import reverse


# Create your views here.

#def index(request):
#	return render(request,forms.Author,'downloads/landing.html')

#def download(request):
#	return render(request,'downloads/index.html',{'obj':Books.objects.values('Author').distinct()})

def Author_redirect(request,name):
	if request.method == 'POST':
		selected_author = request.POST.get('get_book')
		selected_author = [selected_author]
		return redirect(reverse('books',args=selected_author))


	return render(request,'downloads/index.html',{'name':Books.objects.values('Author').filter(Author__contains=name).distinct().annotate(Title_count=Count('Title'))})

def books_redirect(request,name):
	return render(request, 'downloads/book_detail.html',{'name':Books.objects.values('Title','Mirrors').filter(Author__contains=name).distinct()})