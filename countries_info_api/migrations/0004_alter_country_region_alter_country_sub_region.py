# Generated by Django 5.2 on 2025-05-07 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries_info_api', '0003_alter_country_cca3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_countries', to='countries_info_api.region'),
        ),
        migrations.AlterField(
            model_name='country',
            name='sub_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subregion_countries', to='countries_info_api.subregion'),
        ),
    ]
