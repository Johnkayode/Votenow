# Generated by Django 3.1.4 on 2020-12-27 14:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_auto_20201226_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 15, 48, 23, 616706)),
        ),
    ]
