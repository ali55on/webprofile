# Generated by Django 4.1.1 on 2022-10-08 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webprofile', '0027_alter_post_review_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='review_reason',
            field=models.TextField(blank=True, default='Sinalizado como sensível', max_length=105, null=True),
        ),
    ]
