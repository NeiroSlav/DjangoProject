# Generated by Django 4.2.5 on 2023-09-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='theme',
        ),
        migrations.AddField(
            model_name='customuser',
            name='settings',
            field=models.JSONField(default=False, verbose_name='settings'),
        ),
    ]
