# Generated by Django 5.0.3 on 2024-05-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('is_posted', models.BooleanField(default=False, verbose_name='Posted')),
            ],
        ),
        migrations.CreateModel(
            name='NominationPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('is_posted', models.BooleanField(default=False, verbose_name='Posted')),
            ],
        ),
    ]