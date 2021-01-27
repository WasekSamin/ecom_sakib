# Generated by Django 3.1.5 on 2021-01-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210123_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSpces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec_title', models.CharField(max_length=155)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='store.ProductColors'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, to='store.ProductSizes'),
        ),
        migrations.AddField(
            model_name='product',
            name='spec',
            field=models.ManyToManyField(blank=True, to='store.ProductSpces'),
        ),
    ]
