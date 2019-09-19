from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Books
from .forms import AuthorForm
from django.db.models import Count
from django.forms import ModelForm
from django.urls import reverse
import time
import logging
from .functions import request_multithread, request_w_proxies, scrape, make_dict_get_urls
from django.utils import timezone
from django.views import View


logger = logging.getLogger(__name__)




def index(request):
    submitted = False
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # add book name search functionality
            start = time.time()
            cd = form['A_Name'].value()
            name = [cd]
            if Books.objects.filter(Author__contains=cd).exists():
                end = time.time()
                logger.error('total'+' ' +str(end-start))
                return redirect(reverse('Author',args=name))
            else:

                hold = make_dict_get_urls(cd)

                for x in hold:
                    #function?
                    p = Books(
                    ID=x['ID'],
                    Author=x['Author(s)'],
                    Title=x['Title'],
                    Publisher=x['Publisher'],
                    Year_published=x['Year'],
                    num_Pages=x['Pages'],
                    Language=x['Language'],
                    Size=x['Size'],
                    Extension=x['Extension'],
                    Mirrors=x['Mirrors'],
                    Edit=x['Edit'],
                    created_at =timezone.now()
                    )
                    p.save()
                end = time.time()
                logger.error('total'+' ' +str(end-start))
                return redirect(reverse('Author',args=name))
    else:
        form = AuthorForm()
        if 'submitted' in request.GET:
            submitted = True

    #send it to appropriate views file that will use form data
    return render(request,'downloads/landing.html',{'form': form, 'submitted':submitted})

def Author_redirect(request,name):
    if request.method == 'POST':
        selected_author = request.POST.get('get_book')
        selected_author = [selected_author]
        return redirect(reverse('books',args=selected_author))


    return render(request,'downloads/index.html',{'name':Books.objects.values('Author').filter(Author__contains=name).distinct().annotate(Title_count=Count('Title'))})




def books_redirect(request,name):
    return render(request, 'downloads/book_detail.html',{'name':Books.objects.values('Title','Mirrors').filter(Author__contains=name).distinct()})


