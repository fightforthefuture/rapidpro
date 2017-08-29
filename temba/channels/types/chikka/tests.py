from __future__ import unicode_literals, absolute_import

from django.urls import reverse
from temba.tests import TembaTest
from ...models import Channel


class ChikkaTypeTest(TembaTest):

    def test_claim(self):
        Channel.objects.all().delete()

        url = reverse('channels.claim_chikka')

        self.login(self.admin)

        response = self.client.get(reverse('channels.channel_claim'))
        self.assertNotContains(response, url)

        self.org.timezone = 'Asia/Manila'
        self.org.save()

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse('channels.channel_claim'))
        self.assertContains(response, url)

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.context['view'].get_country({}), 'Philippines')

        post_data = response.context['form'].initial

        post_data['country'] = 'PH'
        post_data['number'] = '5259'
        post_data['username'] = 'chikka'
        post_data['password'] = 'password'

        response = self.client.post(url, post_data)

        channel = Channel.objects.get()

        self.assertEquals('chikka', channel.config_json()[Channel.CONFIG_USERNAME])
        self.assertEquals('password', channel.config_json()[Channel.CONFIG_PASSWORD])
        self.assertEquals('5259', channel.address)
        self.assertEquals('PH', channel.country)
        self.assertEquals('CK', channel.channel_type)

        config_url = reverse('channels.channel_configuration', args=[channel.pk])
        self.assertRedirect(response, config_url)

        response = self.client.get(config_url)
        self.assertEquals(200, response.status_code)

        self.assertContains(response, reverse('handlers.chikka_handler', args=[channel.uuid]))