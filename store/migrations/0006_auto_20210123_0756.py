# Generated by Django 3.1.5 on 2021-01-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210123_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='uoms',
        ),
        migrations.AddField(
            model_name='product',
            name='uoms',
            field=models.ManyToManyField(null=True, to='store.UOM'),
        ),
    ]
