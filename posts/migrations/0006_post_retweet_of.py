# Generated by Django 3.2.12 on 2023-08-14 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_reply_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='retweet_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retweets', to='posts.post'),
        ),
    ]