# Generated by Django 2.1.1 on 2018-09-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20180910_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='courses/%Y/%m', verbose_name='头像'),
        ),
    ]
