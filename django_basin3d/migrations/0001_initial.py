# Generated by Django 3.1 on 2020-08-10 19:50

from django.db import migrations, models
import django.db.models.deletion
import django_basin3d.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('id_prefix', models.CharField(max_length=5, unique=True)),
                ('location', models.TextField(blank=True)),
                ('plugin_module', models.TextField(blank=True)),
                ('plugin_class', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['id_prefix'],
            },
        ),
        migrations.CreateModel(
            name='ObservedPropertyVariable',
            fields=[
                ('basin3d_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('categories', django_basin3d.models.StringListField(blank=True, null=True)),
            ],
            options={
                'ordering': ('basin3d_id',),
            },
        ),
        migrations.CreateModel(
            name='SamplingMedium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservedProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('datasource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_basin3d.datasource')),
                ('observed_property_variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_basin3d.observedpropertyvariable')),
                ('sampling_medium', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_basin3d.samplingmedium')),
            ],
            options={
                'unique_together': {('observed_property_variable', 'datasource')},
            },
        ),
        migrations.CreateModel(
            name='DataSourceObservedPropertyVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('datasource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_basin3d.datasource')),
                ('observed_property_variable', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='django_basin3d.observedpropertyvariable')),
            ],
            options={
                'unique_together': {('datasource', 'observed_property_variable')},
            },
        ),
    ]
