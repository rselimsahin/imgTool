# Generated by Django 2.1.4 on 2018-12-30 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0020_auto_20181228_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='group',
        ),
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.AlterField(
            model_name='image',
            name='rules',
            field=models.CharField(blank=True, default='[]', max_length=1000000),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
