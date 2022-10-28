# Generated by Django 3.1.5 on 2021-02-10 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('category', models.CharField(choices=[('Fiction', 'FICTION'), ('Children', 'CHILDREN'), ('Fantasy', 'FANTASY'), ('NonFiction', 'NON-FICTION'), ('Sci-Fi', 'SCI-FI'), ('Young Adult', 'YOUNG ADULT'), ('Mystery', 'MYSTERY')], default='', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('bids', models.ManyToManyField(blank=True, related_name='bids', to='auctions.Bids')),
                ('comments', models.ManyToManyField(blank=True, null=True, related_name='comments', to='auctions.Comments')),
            ],
        ),
    ]
