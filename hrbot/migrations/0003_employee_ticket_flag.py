# Generated by Django 2.0 on 2018-03-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrbot', '0002_auto_20180323_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='ticket_flag',
            field=models.BooleanField(default=False),
        ),
    ]
