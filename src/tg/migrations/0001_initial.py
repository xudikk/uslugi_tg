# Generated by Django 3.2.7 on 2021-09-07 05:42

from django.db import migrations, models
import tg


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(default=tg.lang_dict_field)),
                ('alias', models.CharField(max_length=32, unique=True)),
                ('sort_order', models.IntegerField(db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('messages', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]