# Generated by Django 2.1.1 on 2018-09-17 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecomments',
            name='comments',
            field=models.CharField(default='', max_length=300, verbose_name='评论'),
        ),
    ]
