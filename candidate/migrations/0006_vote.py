# Generated by Django 5.0.3 on 2024-04-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_auto_20240424_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]