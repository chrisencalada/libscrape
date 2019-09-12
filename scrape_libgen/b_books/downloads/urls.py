from django.urls import path
from django.urls import re_path
from downloads import views
from downloads import forms

urlpatterns = [
#re_path(r'^download/',views.download, name='download'),
#path('Author/', forms.Author,name='Autor'),
path('',forms.Author, name='landing'),
path('Author/<name>/',views.Author_redirect,name='Author'),
path('Author/<name>/books',views.books_redirect,name='books'),

]