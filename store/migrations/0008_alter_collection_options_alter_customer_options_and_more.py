# Generated by Django 5.1.6 on 2025-03-24 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
