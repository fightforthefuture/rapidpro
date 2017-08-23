from __future__ import unicode_literals, absolute_import

from django.urls import reverse
from temba.tests import TembaTest
from ...models import Channel


class AfricastalkingTypeTest(TembaTest):

    def test_claim(self):
        Channel.objects.all().delete()
        self.login(self.admin)

        url = reverse('channels.claim_africastalking')

        # visit the africa's talking page
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        post_data = response.context['form'].initial

        post_data['shortcode'] = '5259'
        post_data['username'] = 'temba'
        post_data['api_key'] = 'asdf-asdf-asdf-asdf-asdf'
        post_data['country'] = 'KE'

        response = self.client.post(url, post_data)

        channel = Channel.objects.get()

        self.assertEquals('temba', channel.config_json()['username'])
        self.assertEquals('asdf-asdf-asdf-asdf-asdf', channel.config_json()['api_key'])
        self.assertEquals('5259', channel.address)
        self.assertEquals('KE', channel.country)
        self.assertEquals('AT', channel.channel_type)

        config_url = reverse('channels.channel_configuration', args=[channel.pk])
        self.assertRedirect(response, config_url)

        response = self.client.get(config_url)
        self.assertEquals(200, response.status_code)

        self.assertContains(response, reverse('handlers.africas_talking_handler', args=['callback', channel.uuid]))
        self.assertContains(response, reverse('handlers.africas_talking_handler', args=['delivery', channel.uuid]))