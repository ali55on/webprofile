# Generated by Django 4.1.1 on 2022-09-15 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webprofile', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='images/generic_image.png', upload_to='images/%d/%m/%Y/'),
        ),
    ]
