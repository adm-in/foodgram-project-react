# Generated by Django 3.0.5 on 2021-07-19 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210719_0858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='value',
            new_name='amount',
        ),
    ]