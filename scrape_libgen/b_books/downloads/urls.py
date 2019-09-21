from django.urls import path
from django.urls import re_path
from downloads import views
from downloads import forms

urlpatterns = [
#re_path(r'^download/',views.download, name='download'),
#path('Author/', forms.Author,name='Autor'),
path('',views.SearchView.as_view(), name='landing'),
path('Author/<name>/',views.AuthorDetailView.as_view(),name='Author'),
path('Author/<name>/books',views.BookDetailView.as_view(),name='books'),

]