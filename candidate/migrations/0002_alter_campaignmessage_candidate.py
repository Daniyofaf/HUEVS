# Generated by Django 5.0.3 on 2024-05-18 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_admincandidatecreation_id_number'),
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignmessage',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.admincandidatecreation'),
        ),
    ]
