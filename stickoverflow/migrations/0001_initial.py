# Generated by Django 2.2.1 on 2019-05-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('file_no', models.IntegerField()),
                ('file_name', models.CharField(max_length=260)),
                ('file_path', models.CharField(max_length=260)),
                ('file_description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Enter User ID', max_length=50)),
                ('file_no', models.IntegerField()),
                ('result_no', models.IntegerField()),
                ('analysis_code', models.IntegerField()),
                ('save_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(help_text='Enter User ID', max_length=50)),
                ('password', models.CharField(help_text='Enter password', max_length=50)),
                ('user_name', models.CharField(help_text='Enter user name', max_length=50)),
                ('email', models.CharField(help_text='Enter email', max_length=100)),
                ('department', models.CharField(help_text='Enter department', max_length=50, null=True)),
                ('input_id', models.CharField(max_length=50)),
                ('input_ip', models.CharField(max_length=15)),
                ('input_data', models.DateTimeField(auto_now=True)),
                ('update_id', models.CharField(max_length=50)),
                ('update_ip', models.CharField(max_length=15)),
                ('update_data', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
