# Generated by Django 3.1.3 on 2020-11-28 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20201128_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='shutter_speed',
            field=models.IntegerField(editable=False, null=True),
        ),
    ]