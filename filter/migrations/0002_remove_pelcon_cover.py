# Generated by Django 3.2.3 on 2021-05-25 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelcon',
            name='cover',
        ),
    ]
