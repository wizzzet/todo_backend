# Generated by Django 3.1.2 on 2020-10-28 19:59

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='first name')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Телефон')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('email_verified_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время подтверждения email')),
                ('restore_salt', models.CharField(blank=True, help_text='Выставляется при запросе восстановления пароля и удаляется после успешной смены пароля, либо по сроку годности', max_length=80, null=True, verbose_name='Соль восстановления пароля')),
                ('restore_salt_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Срок годности соли восстановления')),
                ('restore_token', models.CharField(blank=True, help_text="Выставляется при подтверждении email'а запроса восстановления пароля. Удаляется после успешной смены пароля, либо по сроку годности", max_length=80, null=True, verbose_name='Токен восстановления пароля')),
                ('restore_token_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Срок годности токена восстановления')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]
