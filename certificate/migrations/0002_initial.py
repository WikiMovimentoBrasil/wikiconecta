# Generated by Django 4.2.5 on 2023-09-22 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certificate', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='user_certificate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activitylink',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='activity_link', to='certificate.coursemodule'),
        ),
        migrations.AddField(
            model_name='activitylink',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_activity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='activitylink',
            unique_together={('module', 'user')},
        ),
    ]
