# Generated by Django 3.0.5 on 2021-07-16 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210716_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tagrecipe',
            old_name='post',
            new_name='recipe',
        ),
    ]
