# Generated by Django 4.0.6 on 2022-07-31 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_books_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
    ]
