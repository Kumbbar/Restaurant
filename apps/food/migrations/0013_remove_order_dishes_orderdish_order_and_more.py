# Generated by Django 4.2.1 on 2024-04-11 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_remove_order_table_number_order_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dishes',
        ),
        migrations.AddField(
            model_name='orderdish',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='food.client'),
        ),
        migrations.AlterField(
            model_name='orderdish',
            name='dish',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.dish'),
            preserve_default=False,
        ),
    ]