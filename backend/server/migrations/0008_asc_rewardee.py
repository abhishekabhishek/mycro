# Generated by Django 2.0.6 on 2018-08-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20180709_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='asc',
            name='rewardee',
            field=models.CharField(default='0xfake', max_length=42),
            preserve_default=False,
        ),
    ]
