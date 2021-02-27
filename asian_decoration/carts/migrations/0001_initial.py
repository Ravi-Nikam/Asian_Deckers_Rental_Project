# Generated by Django 3.0.3 on 2020-03-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dec_app', '0003_rel_pro'),
    ]

    operations = [
        migrations.CreateModel(
            name='carts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=5, max_length=100)),
                ('available', models.BooleanField(default=True)),
                ('rel_pros', models.ManyToManyField(blank=True, null=True, to='dec_app.rel_pro')),
            ],
        ),
    ]