# Generated by Django 3.0.5 on 2021-10-26 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210927_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепты', 'verbose_name_plural': 'Рецепты'},
        ),
    ]