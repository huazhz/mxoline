# Generated by Django 2.1.1 on 2018-09-12 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180912_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='students',
            new_name='student',
        ),
    ]