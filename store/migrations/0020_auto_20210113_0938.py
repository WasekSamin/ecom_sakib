# Generated by Django 3.1.5 on 2021-01-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210113_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='st_title',
            field=models.CharField(default='Pending', max_length=155),
        ),
    ]