# Generated by Django 4.1.1 on 2022-09-24 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webprofile', '0016_delete_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
    ]
