# Libscrape
Website can be found here: https://muraki.xyz/

This personal project was made so I could practice web scraping and django.
This project is a libgen clone (https://libgen.is/) where I webscrape libgen for a given author and then return that author's books in an ordered list.
The project uses requests and beautifulsoup to scrape the data and multiprocessing to speed up some requests (this can be found in the functions.py file).
Book and author data is saved in a Postgres database and is returned from that database whenever a request happens.
New data that cannot be found in the database is scraped from the libgen website.
The website is deployed using Nginx,Gunicorn, and Django.

