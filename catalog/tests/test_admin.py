from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            pseudonym="test pseudonym"
        )

    def test_author_pseudonym_listed(self):
        """
        Test that aaa
        :return:
        """
        url = reverse("admin:catalog_author_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)

    def test_author_detail_pseudonym_listed(self):
        """
        Test that aaa
        :return:
        """
        url = reverse("admin:catalog_author_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)
