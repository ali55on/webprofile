# Generated by Django 4.1.1 on 2022-09-13 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formuser',
            name='username',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
