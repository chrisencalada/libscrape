from django.db import models
from simple_history.models import HistoricalRecords
import logging
from .functions import strip_accents
import string
import re

#simple_history creates a mirror table (with a history prefix)
#that will save historical changes to the Books model

# Create your models here.


logger = logging.getLogger(__name__)

class NameField(models.CharField):
    def __init__(self,*args,**kwargs):
        super(NameField,self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        name = str(value)
        translator = str.maketrans('', '', string.punctuation)
        name = strip_accents(name)
        name = name.translate(translator)
        name = " ".join(name.split())
        name = name.rstrip(',')
        name = name.lower()
        name = name.title()
        return name


class Books(models.Model):
    ID = models.IntegerField(primary_key=True)
    Author = NameField(max_length=500)
    Author_original = models.CharField(max_length=500)
    Title = models.CharField(max_length=500)
    Publisher = models.CharField(max_length=500)
    Year_published = models.CharField(max_length=500)
    num_Pages = models.CharField(max_length=500)
    Language = models.CharField(max_length=500)
    Size = models.CharField(max_length=500)
    Extension = models.CharField(max_length=500)
    Mirrors = models.URLField(max_length=5000)
    Edit = models.CharField(max_length=500)
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #def __str__(self):
    #   return self.books.Author