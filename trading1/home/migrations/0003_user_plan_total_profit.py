# Generated by Django 4.2.6 on 2023-10-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_addprofit_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_plan',
            name='total_profit',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
