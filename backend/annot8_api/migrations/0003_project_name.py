# Generated by Django 4.0.4 on 2022-05-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annot8_api', '0002_project_data_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(default='some name', max_length=255),
            preserve_default=False,
        ),
    ]
