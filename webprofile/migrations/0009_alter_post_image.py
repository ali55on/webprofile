# Generated by Django 4.1.1 on 2022-09-18 03:00

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('webprofile', '0008_alter_post_category_alter_post_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 300], upload_to='images/%d/%m/%Y/'),
        ),
    ]
