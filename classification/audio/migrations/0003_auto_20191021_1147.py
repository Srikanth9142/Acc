# Generated by Django 2.2.5 on 2019-10-21 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0002_auto_20191013_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomodel',
            name='prediction',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
