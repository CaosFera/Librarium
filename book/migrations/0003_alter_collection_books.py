# Generated by Django 5.1.3 on 2024-11-17 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_collection_collector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='collections', to='book.book'),
        ),
    ]
