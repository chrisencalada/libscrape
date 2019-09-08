# Generated by Django 2.2.4 on 2019-08-22 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Author', models.CharField(max_length=500)),
                ('Title', models.CharField(max_length=500)),
                ('Publisher', models.CharField(max_length=500)),
                ('Year_published', models.CharField(max_length=500)),
                ('num_Pages', models.CharField(max_length=500)),
                ('Language', models.CharField(max_length=500)),
                ('Size', models.CharField(max_length=500)),
                ('Extension', models.CharField(max_length=500)),
                ('Mirrors', models.URLField(max_length=500)),
                ('Edit', models.CharField(max_length=500)),
            ],
        ),
    ]