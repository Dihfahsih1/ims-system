# Generated by Django 2.1.7 on 2019-03-13 13:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('canonapp', '0008_auto_20190313_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 433853, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='driver_checklist',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 436178, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='driver_payment_report',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 434813, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='driver_payment_reports_archive',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 435688, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='driverpayment',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 434335, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='driverpayments_archive',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 435195, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='expensesreportarchive',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 438354, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 437021, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryreportarchive',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 439337, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='spend',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 437917, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sundry',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 437517, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sundryreportarchive',
            name='Date',
            field=models.DateField(default=datetime.datetime(2019, 3, 13, 13, 55, 45, 438876, tzinfo=utc)),
        ),
    ]
