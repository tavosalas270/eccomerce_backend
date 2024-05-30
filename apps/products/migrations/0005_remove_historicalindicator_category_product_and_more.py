# Generated by Django 5.0.3 on 2024-05-18 14:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_historicalcategoryproduct_historicalindicator_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalindicator",
            name="category_product",
        ),
        migrations.RemoveField(
            model_name="historicalindicator",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalmeasureunit",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalproduct",
            name="category_product",
        ),
        migrations.RemoveField(
            model_name="historicalproduct",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalproduct",
            name="measure_unit",
        ),
        migrations.DeleteModel(
            name="HistoricalCategoryProduct",
        ),
        migrations.DeleteModel(
            name="HistoricalIndicator",
        ),
        migrations.DeleteModel(
            name="HistoricalMeasureUnit",
        ),
        migrations.DeleteModel(
            name="HistoricalProduct",
        ),
    ]