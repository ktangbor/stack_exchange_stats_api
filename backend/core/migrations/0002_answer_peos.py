# Generated by Django 4.1.3 on 2023-05-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='peos',
            field=models.CharField(max_length=21, null=True),
        ),
    ]