# Generated by Django 2.1.7 on 2019-03-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190306_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='dob',
            field=models.DateField(default='2019-03-12'),
        ),
    ]
