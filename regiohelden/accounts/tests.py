import json

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User as DjangoUser

from rest_framework.reverse import reverse

from accounts.models import User


class UsersApiIntegrationTest(TestCase):
    def setUp(self):
        self.admin1 = DjangoUser.objects.create(
            username='admin1', is_staff=True, is_superuser=True)
        self.admin1.set_password('admin1')
        self.admin1.save()

        self.admin2 = DjangoUser.objects.create(
            username='admin2', is_staff=True, is_superuser=True)
        self.admin2.set_password('admin2')
        self.admin2.save()

        self.unauth_client = Client()
        self.admin1_client = Client()
        self.admin1_client.login(username='admin1', password='admin1')
        self.admin2_client = Client()
        self.admin2_client.login(username='admin2', password='admin2')

        self.users_url = '/api/1.0/users/'

    def test_get_users(self):
        user1 = User.objects.create(
            first_name='user1 first', 
            last_name='user1 last', 
            iban='DE89370400440532013000',
            creator=self.admin1)
        user2 = User.objects.create(
            first_name='user2 first', 
            last_name='user2 last', 
            iban='BE68539007547034',
            creator=self.admin2)

        self.assertEquals(
            self.unauth_client.get(self.users_url).status_code, 403)

        response = self.admin1_client.get(self.users_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 2)
        self.assertEquals(response.json()['results'], [
            {'iban': 'DE89370400440532013000', 
            'last_name': 'user1 last', 
            'id': user1.id, 
            'first_name': 'user1 first', 
            'creator': {'username': 'admin1', 'id': self.admin1.id}}, 
            {'iban': 'BE68539007547034', 
            'last_name': 'user2 last', 
            'id': user2.id, 
            'first_name': 'user2 first', 
            'creator': {'username': 'admin2', 'id': self.admin2.id}}],)

        self.assertEquals(
            self.admin2_client.get(self.users_url).content, response.content)

    def test_post_users(self):
        valid_user_data = {
            'first_name': 'Some', 
            'last_name': 'Other', 
            'iban': 'BE68539007547034'}
        invalid_iban_user_data = {
            'first_name': 'Some', 
            'last_name': 'Other', 
            'iban': 'BE68539007547022'}
        too_long_name_user_data = {
            'first_name': '1' * 101, 
            'last_name': 'Other', 
            'iban': 'BE68539007547034'}
        missed_field_user_data = {
            'first_name': 'Some',
            'iban': 'BE68539007547034'}

        self.assertEquals(
            self.unauth_client.post(
                self.users_url, valid_user_data).status_code, 403)

        response = self.admin1_client.post(self.users_url, valid_user_data)
        self.assertEquals(response.status_code, 201)
        data = response.json()
        self.assertEquals(data['first_name'], 'Some')
        self.assertEquals(data['last_name'], 'Other')
        self.assertEquals(data['iban'], 'BE68539007547034')
        self.assertEquals(data['creator']['username'], 'admin1')

        response = self.admin2_client.post(self.users_url, valid_user_data)
        self.assertEquals(response.status_code, 201)
        data = response.json()
        self.assertEquals(data['first_name'], 'Some')
        self.assertEquals(data['last_name'], 'Other')
        self.assertEquals(data['iban'], 'BE68539007547034')
        self.assertEquals(data['creator']['username'], 'admin2')

        response = self.admin1_client.post(
            self.users_url, invalid_iban_user_data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.json(), {'iban': ['Not a valid IBAN.']})

        response = self.admin1_client.post(
            self.users_url, too_long_name_user_data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.json(), 
            {'first_name': 
            ['Ensure this field has no more than 100 characters.']})

        response = self.admin1_client.post(
            self.users_url, missed_field_user_data)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.json(), {'last_name': ['This field is required.']})

    def test_delete_user(self):
        user = User.objects.create(
            first_name='user1 first', 
            last_name='user1 last', 
            iban='DE89370400440532013000',
            creator=self.admin1)

        user_url = '{}{}/'.format(self.users_url, user.id)

        self.assertEquals(
            self.unauth_client.delete(user_url).status_code, 403)

        self.assertEquals(
            self.admin2_client.delete(user_url).status_code, 403)

        response = self.admin1_client.delete(user_url)
        self.assertEquals(response.status_code, 204)

    def test_patch_user(self):
        user = User.objects.create(
            first_name='user1 first', 
            last_name='user1 last', 
            iban='DE89370400440532013000',
            creator=self.admin1)
        valid_data = {
            'first_name': 'Other name', 
            'last_name': 'New name',
            'iban': 'BE68539007547034'}
        invalid_iban_user_data = {
            'first_name': 'Some', 
            'last_name': 'Other', 
            'iban': 'BE68539007547022'}
        too_long_name_user_data = {
            'first_name': '1' * 101, 
            'last_name': 'Other', 
            'iban': 'BE68539007547034'}
        data_with_read_only_fields = {
            'first_name': 'Other name', 
            'last_name': 'New name',
            'iban': 'BE68539007547034',
            'creator': {'id': self.admin2.id, 'username': 'admin2'}}

        user_url = '{}{}/'.format(self.users_url, user.id)

        self.assertEquals(
            self.unauth_client.patch(user_url, valid_data).status_code, 403)

        self.assertEquals(
            self.admin2_client.patch(user_url, valid_data).status_code, 403)

        response = self.admin1_client.patch(
            user_url, json.dumps(invalid_iban_user_data), 
            content_type='application/json')
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.json(), {'iban': ['Not a valid IBAN.']})

        response = self.admin1_client.patch(
            user_url, json.dumps(too_long_name_user_data), 
            content_type='application/json')
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.json(), 
            {'first_name': 
            ['Ensure this field has no more than 100 characters.']})

        response = self.admin1_client.patch(
            user_url, json.dumps(data_with_read_only_fields), 
            content_type='application/json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.json(), 
            {'creator': {'username': 'admin1', 'id': self.admin1.id}, 
            'last_name': 'New name', 'iban': 'BE68539007547034', 
            'id': 4, 'first_name': 'Other name'})








