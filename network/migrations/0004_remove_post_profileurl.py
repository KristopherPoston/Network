# Generated by Django 5.0.7 on 2024-11-20 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_profileurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profileUrl',
        ),
    ]
