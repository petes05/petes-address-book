# Generated by Django 2.1.1 on 2018-09-23 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0002_auto_20180922_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='first_line',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
