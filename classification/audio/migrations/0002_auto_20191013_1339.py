# Generated by Django 2.2.5 on 2019-10-13 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomodel',
            name='prediction',
            field=models.CharField(max_length=70, null=True),
        ),
    ]