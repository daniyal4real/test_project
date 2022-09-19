# Generated by Django 4.1.1 on 2022-09-15 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=70)),
                ('description', models.CharField(default='', max_length=300)),
                ('producer', models.CharField(default='', max_length=50)),
                ('rating', models.FloatField()),
                ('published', models.BooleanField(default=False)),
            ],
        ),
    ]
