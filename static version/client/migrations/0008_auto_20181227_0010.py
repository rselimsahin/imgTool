# Generated by Django 2.1.4 on 2018-12-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_auto_20181227_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='gname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
