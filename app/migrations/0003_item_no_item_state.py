# Generated by Django 4.1.13 on 2024-03-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_item_count_item_deadline_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='no',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]