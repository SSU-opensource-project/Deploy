# Generated by Django 3.2.9 on 2021-12-02 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_posting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
