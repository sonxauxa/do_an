# Generated by Django 3.2.3 on 2021-05-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0006_auto_20210525_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelcon',
            name='pdf',
            field=models.FileField(upload_to='store/pdfs/'),
        ),
    ]
