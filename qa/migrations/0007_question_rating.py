# Generated by Django 2.1.7 on 2019-04-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20190415_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]