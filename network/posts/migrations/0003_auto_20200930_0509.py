# Generated by Django 3.1.1 on 2020-09-30 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200930_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post'),
        ),
    ]
