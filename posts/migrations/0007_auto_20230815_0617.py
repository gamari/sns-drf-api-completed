# Generated by Django 3.2.12 on 2023-08-14 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_retweet_of'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='retweet_of',
        ),
        migrations.AddField(
            model_name='post',
            name='repost_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reposts', to='posts.post'),
        ),
    ]
