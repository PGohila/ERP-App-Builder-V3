# Generated by Django 4.2.7 on 2024-02-13 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0017_model_identification'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainsubmenu',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sub_part.project'),
        ),
    ]
