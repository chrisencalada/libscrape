from django.db import models
from simple_history.models import HistoricalRecords

#simple_history creates a mirror table (with a history prefix)
#that will save historical changes to the Books model

# Create your models here.
class Books(models.Model):
	ID = models.IntegerField(primary_key=True)
	Author = models.CharField(max_length=500)
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
	#	return self.books.Author