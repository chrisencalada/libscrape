from django.urls import path
from django.urls import re_path
from . import views
from . import forms

urlpatterns = [
#re_path(r'^download/',views.download, name='download'),
#path('Author/', forms.Author,name='Autor'),
path('',forms.Author, name='Author'),

]