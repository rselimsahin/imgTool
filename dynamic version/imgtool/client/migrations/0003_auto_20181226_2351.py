# Generated by Django 2.1.4 on 2018-12-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20181226_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True,  primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='uname',
            field=models.CharField(default='', max_length=30),
        ),
    ]
