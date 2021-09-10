# Generated by Django 3.2.7 on 2021-09-08 08:30

import base.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.JSONField(blank=True, default=base.fields.lang_dict_field, null=True)),
                ('sort_order', models.IntegerField(db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.JSONField(blank=True, default=base.fields.lang_dict_field, null=True)),
                ('sort_order', models.IntegerField(db_index=True, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_region', to='geo.region')),
            ],
        ),
    ]