# Generated by Django 4.2.8 on 2023-12-22 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0012_screenversionfields_column_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenversionfields',
            name='label_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
