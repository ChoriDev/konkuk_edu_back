# Generated by Django 4.1.13 on 2024-03-17 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_item_state'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('no', 'name'), name='물품별 고유 번호 부여'),
        ),
    ]
