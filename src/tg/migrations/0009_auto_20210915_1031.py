# Generated by Django 3.2.7 on 2021-09-15 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0008_announce'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announce',
            name='category',
        ),
        migrations.CreateModel(
            name='AnnounceCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announce_categories', to='tg.category')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announce_categories_m', to='tg.announce')),
            ],
        ),
    ]
