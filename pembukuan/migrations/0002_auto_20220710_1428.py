# Generated by Django 4.0.5 on 2022-07-10 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pembukuan', '0001_initial'),
    ]

    def insert_default_category(apps, schema_editor):
        Category = apps.get_model('pembukuan', 'category')
        category_pemasukan = Category(name='Pemasukan')
        category_pemasukan.save()
        category_pengeluaran = Category(name='Pengeluaran')
        category_pengeluaran.save()
        category_lain = Category(name='Lain-lain')
        category_lain.save()

    operations = [
        migrations.RunPython(insert_default_category)
    ]
