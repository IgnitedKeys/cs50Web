# Generated by Django 3.1.5 on 2021-02-15 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listings_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listings',
            name='lister',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='listers', to='auctions.user'),
            preserve_default=False,
        ),
    ]
