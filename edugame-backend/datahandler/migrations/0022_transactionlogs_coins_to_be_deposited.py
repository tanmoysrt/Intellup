# Generated by Django 3.2.5 on 2021-07-09 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datahandler', '0021_coinpackages'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionlogs',
            name='coins_to_be_deposited',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
