# Generated by Django 3.1.4 on 2021-01-05 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210106_0019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone_number',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]