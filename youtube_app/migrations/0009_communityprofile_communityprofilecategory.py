# Generated by Django 2.2.24 on 2022-10-04 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_app', '0008_auto_20221004_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityProfileCategory',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default='', max_length=300)),
            ],
            options={
                'verbose_name': 'community Profile Categories',
                'verbose_name_plural': 'community Profile Categories',
            },
        ),
        migrations.CreateModel(
            name='CommunityProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000)),
                ('avatar_image', models.ImageField(blank=True, null=True, upload_to='upload_images/', verbose_name='Avatar')),
                ('banner_image', models.ImageField(default='upload_images/default.png', upload_to='upload_images/', verbose_name='Banner Image')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('experience', models.CharField(blank=True, max_length=400, null=True)),
                ('bio', models.CharField(max_length=500)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtube_app.Keyword')),
                ('profile_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youtube_app.CommunityProfileCategory')),
            ],
            options={
                'verbose_name': 'Community Profiles',
                'verbose_name_plural': 'Community Profiles',
            },
        ),
    ]
