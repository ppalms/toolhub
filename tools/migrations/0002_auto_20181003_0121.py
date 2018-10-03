# Generated by Django 2.1.1 on 2018-10-03 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Create'), (1, 'Borrow'), (2, 'Return'), (3, 'Decommission'), (4, 'Reinstate')])),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='usertool',
            name='visibility',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Visible to owner'), (1, 'Visible to cleared'), (2, 'Visbile to everyone')], default=2, verbose_name='Visibility'),
        ),
        migrations.AlterField(
            model_name='usertool',
            name='clearance',
            field=models.PositiveSmallIntegerField(choices=[(0, 'No clearance'), (1, 'Owner approved'), (2, 'Cleared-user approved')], default=0, verbose_name='Clearance'),
        ),
        migrations.AddField(
            model_name='toolhistory',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.UserTool'),
        ),
        migrations.AddField(
            model_name='toolhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
