from django import forms
from django.forms import ModelForm
from .models import Books

#core
#1. make author names into slugs
#2. 
#2. connect that view to the render command at the end of the form.py
#1. if more than 10 pages of results our if statement doesn't work anymore
#1. check why sometimes you get nonetype failures
#NoneType' object is not subscriptable
#1. clean up the author names so that same name does not show as distinct
#3. mass download link? 
#4. add a function to expire stale data
#5. set up a data pipeline to download weekly data dumps from libgen and load them into database
#6. host this online??
#7. fix mirror site logic (download all 5 mirrors? then loop through them until you find one that doesnt 503?) 




class AuthorForm(forms.Form):
    A_Name = forms.CharField(label='Author Name',max_length=100)

