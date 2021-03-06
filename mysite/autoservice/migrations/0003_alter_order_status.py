# Generated by Django 3.2 on 2021-05-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0002_auto_20210504_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('draft', 'Draft'), ('in progress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled')], default='d', help_text='Status', max_length=12),
        ),
    ]
