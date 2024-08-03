# Generated by Django 5.0.6 on 2024-06-15 06:37

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_consultation_name'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='default.png', null=True, upload_to='author-image')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=280, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('images', models.ImageField(blank=True, null=True, upload_to='post-image/')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=180, null=True, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.author')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
