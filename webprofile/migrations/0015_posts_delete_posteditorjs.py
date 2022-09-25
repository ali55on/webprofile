# Generated by Django 4.1.1 on 2022-09-24 22:20

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('webprofile', '0014_rename_content_posteditorjs_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', tinymce.models.HTMLField()),
            ],
        ),
        migrations.DeleteModel(
            name='PostEditorJs',
        ),
    ]
