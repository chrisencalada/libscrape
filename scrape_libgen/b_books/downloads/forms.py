from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.template import RequestContext
from .models import Books
import logging
import time
from django.db.models import Count
from .functions import request_multithread, request_w_proxies, scrape, make_dict_get_urls

#core
# write log files to file?
#1. if more than 10 pages of results our if statement doesn't work anymore
#1. check why sometimes you get nonetype failures
#NoneType' object is not subscriptable
#1. clean up the author names so that same name does not show as distinct
#3. mass download link? 
#4. add a function to expire stale data
#5. set up a data pipeline to download weekly data dumps from libgen and load them into database
#6. host this online??
#7. fix mirror site logic (download all 5 mirrors? then loop through them until you find one that doesnt 503?) 

logger = logging.getLogger(__name__)



class AuthorForm(forms.Form):
    A_Name = forms.CharField(label='Author Name',max_length=100)

#@csrf_exempt
def Author(request):
    submitted = False
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # add book name search functionality
            start = time.time()
            cd = form['A_Name'].value()
            check = make_dict_get_urls(cd)
            hold = check

            #2.
            for x in hold:
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
            #3. return only a distinct list of authors whose name matches entered name
            
            #assert False
            end = time.time()
            logger.error('total'+' ' +str(end-start))
            return render(request,'downloads/index.html',{'name':Books.objects.values('Author').filter(Author__contains=cd).distinct().annotate(Title_count=Count('Title'))})

    else:
        form = AuthorForm()
        if 'submitted' in request.GET:
            submitted = True

    #send it to appropriate views file that will use form data
    return render(request,'downloads/landing.html',{'form': form, 'submitted':submitted})


