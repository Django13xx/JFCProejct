# Generated by Django 5.0 on 2024-01-25 05:31

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='activeHeartAudio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('heart_audio_id', models.IntegerField(default=0)),
                ('heart_audio_name', models.CharField(max_length=200)),
                ('heart_audio_type', models.CharField(default='undefined', max_length=20)),
                ('heart_audio_description', models.CharField(default='', max_length=500)),
                ('heart_audio_level', models.CharField(default='All levels', max_length=20)),
                ('heart_audio_link', models.CharField(max_length=200)),
                ('heart_audio_list', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='activeLungAudio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lung_audio_id', models.IntegerField(default=0)),
                ('lung_audio_name', models.CharField(max_length=200)),
                ('lung_audio_type', models.CharField(default='undefined', max_length=20)),
                ('lung_audio_description', models.CharField(default='', max_length=500)),
                ('lung_audio_level', models.CharField(default='All levels', max_length=20)),
                ('lung_audio_link', models.CharField(max_length=200)),
                ('lung_audio_list', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='audio',
            fields=[
                ('audio_id', models.IntegerField(primary_key=True, serialize=False)),
                ('audio_name', models.CharField(max_length=200)),
                ('audio_type', models.CharField(default='undefined', max_length=20)),
                ('audio_description', models.CharField(default='', max_length=500)),
                ('audio_level', models.CharField(default='All levels', max_length=20)),
                ('audio_link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='audioList',
            fields=[
                ('list_id', models.AutoField(primary_key=True, serialize=False)),
                ('list_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='listContent',
            fields=[
                ('content_id', models.AutoField(primary_key=True, serialize=False)),
                ('list_id', models.IntegerField(default=0)),
                ('list_name', models.CharField(max_length=200)),
                ('audio_id', models.IntegerField(default=0)),
                ('audio_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('question_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=200)),
                ('user_password', models.CharField(max_length=20)),
                ('user_log_state', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
