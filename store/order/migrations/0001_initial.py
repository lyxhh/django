# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=6)),
                ('oaddress', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to='user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='order.OrderInfo'),
        ),
    ]
