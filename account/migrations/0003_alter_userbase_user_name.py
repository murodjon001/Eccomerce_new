# Generated by Django 4.1.5 on 2023-01-25 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userbase_is_active_alter_userbase_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='user_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
