# Generated by Django 3.2.8 on 2021-12-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='due_back',
            field=models.DateField(blank=True, null=True, verbose_name='Срок годности до:'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Введите жанр книги', max_length=200, verbose_name='Имя'),
        ),
    ]