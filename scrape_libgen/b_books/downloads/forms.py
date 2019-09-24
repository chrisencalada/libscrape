from django import forms
from django.forms import ModelForm
from .models import Books

#4. add a function to expire stale data
#5. set up a data pipeline to download weekly data dumps from libgen and load them into database
#6. host this online??
#7. fix mirror site logic (download all 5 mirrors? then loop through them until you find one that doesnt 503?) 




class AuthorForm(forms.Form):
    A_Name = forms.CharField(label='Author Name',max_length=100)

class AuthorSelectForm(forms.Form):
	Author_Name = forms.CharField(label='Authors Selected',max_length=100)
	Book_Count = forms.IntegerField()
	Get_Book = forms.BooleanField()