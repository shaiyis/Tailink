# Generated by Django 3.2.25 on 2025-06-23 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('about', models.TextField(blank=True)),
                ('picture', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='unspecified', max_length=20)),
                ('age', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=100)),
                ('about_me', models.TextField()),
                ('picture', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.BigIntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('dog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='owner.dog')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='owner.owner')),
            ],
        ),
        migrations.AddField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='owner.owner'),
        ),
    ]
