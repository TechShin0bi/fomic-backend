# Generated by Django 4.2.16 on 2024-11-08 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='validated_by',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_admin': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validated_withdrawals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deposit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deposit',
            name='validated_by',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validated_deposits', to=settings.AUTH_USER_MODEL),
        ),
    ]
