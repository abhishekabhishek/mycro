# Generated by Django 2.0.6 on 2018-09-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_auto_20180906_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='symbol',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]