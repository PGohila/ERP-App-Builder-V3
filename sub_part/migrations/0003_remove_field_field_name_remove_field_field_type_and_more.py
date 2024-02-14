# Generated by Django 4.2.5 on 2023-12-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0002_checkbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='field_name',
        ),
        migrations.RemoveField(
            model_name='field',
            name='field_type',
        ),
        migrations.RemoveField(
            model_name='field',
            name='required',
        ),
        migrations.RemoveField(
            model_name='table',
            name='allow_markdown',
        ),
        migrations.RemoveField(
            model_name='table',
            name='decimal_places',
        ),
        migrations.RemoveField(
            model_name='table',
            name='file_upload_limit',
        ),
        migrations.RemoveField(
            model_name='table',
            name='help_text',
        ),
        migrations.RemoveField(
            model_name='table',
            name='image_height',
        ),
        migrations.RemoveField(
            model_name='table',
            name='image_width',
        ),
        migrations.RemoveField(
            model_name='table',
            name='is_required',
        ),
        migrations.RemoveField(
            model_name='table',
            name='max_digits',
        ),
        migrations.RemoveField(
            model_name='table',
            name='max_length',
        ),
        migrations.RemoveField(
            model_name='table',
            name='min_length',
        ),
        migrations.RemoveField(
            model_name='table',
            name='protocol',
        ),
        migrations.RemoveField(
            model_name='table',
            name='select_db_table',
        ),
        migrations.RemoveField(
            model_name='table',
            name='use_autonow',
        ),
        migrations.RemoveField(
            model_name='table',
            name='use_checkbox',
        ),
        migrations.RemoveField(
            model_name='table',
            name='use_date',
        ),
        migrations.RemoveField(
            model_name='table',
            name='use_file_upload',
        ),
        migrations.RemoveField(
            model_name='table',
            name='use_seconds',
        ),
        migrations.AddField(
            model_name='field',
            name='allow_markdown',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='decimal_places',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='file_upload_limit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='help_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='image_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='image_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='field',
            name='max_digits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='min_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='protocol',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='select_db_table',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='use_autonow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='use_checkbox',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='use_date',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='use_file_upload',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='use_seconds',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='table',
            name='field_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='field_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='required',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
