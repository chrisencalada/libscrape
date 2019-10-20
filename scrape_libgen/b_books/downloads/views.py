from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Books
from .forms import AuthorForm
from django.db.models import Count
from django.forms import ModelForm
from django.urls import reverse
import re
import time
import logging
from .functions import request_multithread, request_w_proxies, scrape, make_dict_get_urls
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.views.generic import (CreateView, DetailView, ListView, TemplateView,
                                  UpdateView, FormView)



logger = logging.getLogger(__name__)


# Create your views here.

class SearchView(FormView):
    form_class = AuthorForm
    template_name = 'downloads/landing.html'

    def form_valid(self,form):
        cd = form['A_Name'].value()
        name = [cd]
        #play around with queryset to see how the ORM constructs sql queries
        queryset_1 = Books.objects.values('Author').filter(Author__icontains=cd).distinct().filter(Title__gt=10).annotate(Title_count=Count('Title'))
        logger.error(queryset_1.query)
        #authors that have more than 10 books are considered already scraped and will not be scraped again
        if Books.objects.values('Author').filter(Author__icontains=cd).distinct().annotate(Title_count=Count('Title')).filter(Title_count__gte=10).exists():
                return redirect(reverse('Author',args=name))
        else:
            start = time.time()
            normalized_authors = make_dict_get_urls(cd)
            end = time.time()
            logger.error('total' +' '+ str(end-start))
            #check all keys in normalized_authors to see if they exist in the database
            #book_in_database = Books.objects.values_list('ID').filter(Author__contains=cd)
            #logger.error(book_in_database)

            # add a bulk update method for records that need to be updated
            # need to add staging tables and production tables in database

            Books.objects.bulk_create([Books(**{
                    'ID':x['ID'],
                    'Author':x['Author(s)'],
                    'Author_original' : x['Author_original'],
                    'Title':x['Title'],
                    'Publisher':x['Publisher'],
                    'Year_published':x['Year'],
                    'num_Pages':x['Pages'],
                    'Language':x['Language'],
                    'Size':x['Size'],
                    'Extension':x['Extension'],
                    'Mirrors':x['Mirrors'],
                    'Edit':x['Edit'],
                    'created_at':timezone.now()
                    }) for x in normalized_authors

                    ],ignore_conflicts=True)


            return redirect(reverse('Author',args=name))



#can we replace this with a formview?
class AuthorDetailView(View):
    def get(self, request, *args, **kwargs):
        name = self.kwargs
        name = name['name']
        logger.error(name)
        return render(request,'downloads/index.html',{'name':Books.objects.values('Author').filter(Author__icontains=name).distinct().annotate(Title_count=Count('Title')).order_by('-Title_count')}) 

    def post(self, request, *args, **kwargs):
        selected_author = request.POST.getlist('get_book')
        selected_author = [selected_author]
        logger.error('request: '+str(selected_author))
        return redirect(reverse('books',args=selected_author))



class BookDetailView(TemplateView):

    template_name = 'downloads/book_detail.html'
    
    def get_context_data(self,**kwargs):
        name = super().get_context_data(**kwargs)
        name = name['name']
        names = name.strip('[]')
        names = names.split(',')
        queryset = {'name':Books.objects.values('Title','Mirrors').filter(Author__in=names).distinct()}
        logger.error('query: '+str(queryset['name'].query))
        return queryset




