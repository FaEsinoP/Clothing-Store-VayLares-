# Generated by Django 4.1.2 on 2023-03-24 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0002_alter_orders_time_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='time_accept',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 25, 8, 27, 14, 495801, tzinfo=datetime.timezone.utc), verbose_name='Принят в пункте выдачи'),
        ),
    ]
