# Generated by Django 5.1.6 on 2025-02-23 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_provider_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('borrower', 'Borrower'), ('provider', 'Provider')], max_length=20, null=True),
        ),
    ]
