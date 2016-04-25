# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from temba.utils import chunk_list
import django.utils.timezone


INDEX_SQL = """
CREATE INDEX channels_channelevent_api_view ON channels_channelevent(org_id, contact_id, created_on DESC, id DESC);
"""


def migrate_from_calls(apps, schema_editor):
    Call = apps.get_model('msgs', 'Call')
    ChannelEvent = apps.get_model('channels', 'ChannelEvent')

    call_ids = list(Call.objects.values_list('pk', flat=True))
    num_created = 0

    for call_id_batch in chunk_list(call_ids, 1000):
        call_batch = list(Call.objects.filter(pk__in=call_id_batch))
        event_batch = []

        for call in call_batch:
            event_batch.append(ChannelEvent(event_type=call.call_type,
                                            time=call.time,
                                            duration=call.duration,
                                            created_on=call.created_on,
                                            is_active=call.is_active,
                                            channel_id=call.channel_id,
                                            contact_id=call.contact_id,
                                            org_id=call.org_id))
        ChannelEvent.objects.bulk_create(event_batch)
        num_created += len(event_batch)

        print("Migrated %d of %d calls to channel events" % (num_created, len(call_ids)))


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0035_auto_20160414_0642'),
        ('orgs', '0017_auto_20160301_0513'),
        ('channels', '0031_auto_20160414_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(help_text='The type of event', max_length=16, verbose_name='Event Type', choices=[('unknown', 'Unknown Call Type'), ('mt_call', 'Outgoing Call'), ('mt_miss', 'Missed Outgoing Call'), ('mo_call', 'Incoming Call'), ('mo_miss', 'Missed Incoming Call')])),
                ('time', models.DateTimeField(help_text='When this event took place', verbose_name='Time')),
                ('duration', models.IntegerField(default=0, help_text='Duration in seconds if event is a call', verbose_name='Duration')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, help_text='When this event was created', verbose_name='Created On')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this item is active, use this instead of deleting')),
                ('channel', models.ForeignKey(verbose_name='Channel', to='channels.Channel', help_text='The channel on which this event took place')),
                ('contact', models.ForeignKey(related_name='channel_events', verbose_name='Contact', to='contacts.Contact', help_text='The contact associated with this event')),
                ('org', models.ForeignKey(verbose_name='Org', to='orgs.Org', help_text='The org this event is connected to')),
            ],
        ),
        migrations.RunPython(migrate_from_calls),
        migrations.RunSQL(INDEX_SQL)
    ]
