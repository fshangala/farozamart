# Generated by Django 4.2.7 on 2024-01-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='becomeseller',
            name='trade_licence',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=200),
        ),
    ]
