# Generated by Django 4.2.7 on 2024-01-22 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_categorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.categorymodel'),
        ),
    ]