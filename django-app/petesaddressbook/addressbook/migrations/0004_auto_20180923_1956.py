# Generated by Django 2.1.1 on 2018-09-23 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0003_auto_20180923_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='addressbook.Contact'),
        ),
    ]
