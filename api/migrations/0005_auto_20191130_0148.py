# Generated by Django 2.2.7 on 2019-11-29 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191130_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='written_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]