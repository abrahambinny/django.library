# Generated by Django 4.0.6 on 2022-08-01 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_books_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='author',
        ),
        migrations.AddField(
            model_name='books',
            name='author',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='language',
            field=models.CharField(db_index=True, default='eng', max_length=10),
        ),
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='Authors',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
