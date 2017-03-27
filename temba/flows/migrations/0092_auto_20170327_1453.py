# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def populate_flowstart_participant_count(apps, schema_editor):
    FlowStart = apps.get_model('flows', 'FlowStart')
    FlowStart.objects.update(participant_count=models.F('contact_count'))


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0058_remove_contactgroup_count'),
        ('flows', '0091_auto_20170228_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Contact')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flows.FlowStart')),
            ],
        ),
        migrations.AddField(
            model_name='flowstart',
            name='participants',
            field=models.ManyToManyField(help_text='The contacts who were started down the flow', related_name='flowstarts', through='flows.FlowParticipant', to='contacts.Contact', verbose_name='Participants'),
        ),
        migrations.AddField(
            model_name='flowstart',
            name='participant_count',
            field=models.IntegerField(default=0, help_text='How many unique contacts were started down the flow'),
        ),
        migrations.AddField(
            model_name='flowstart',
            name='purged',
            field=models.BooleanField(default=False, help_text='If the empty runs for this broadcast have been purged'),
        ),
        migrations.RunPython(populate_flowstart_participant_count),
    ]
