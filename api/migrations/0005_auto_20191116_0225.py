# Generated by Django 2.2.7 on 2019-11-15 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191116_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='dish',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
