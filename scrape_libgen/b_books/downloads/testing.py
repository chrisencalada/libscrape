from django.db import migrations, models
import json
from datetime import datetime


#Books = apps.get_model('downloads','Books')

def open_html(path):
    with open(path, 'r') as f:
        return json.load(f)

data = open_html('downloads/static/downloads/book_dict')

print(data)
#for row in data:
#	print(row)


