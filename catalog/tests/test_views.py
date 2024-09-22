from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import LiteraryFormat

LITERARY_FORMAT_URL = reverse("catalog:literary-format-list")


class PublicLiteraryFormatTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(LITERARY_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateLiteraryFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_literary_format(self):
        LiteraryFormat.objects.create(name="drama")
        LiteraryFormat.objects.create(name="poetry")
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        literary_formats = LiteraryFormat.objects.all()
        self.assertEqual(
            list(response.context["literary_format_list"]),
            list(literary_formats)
        )
        self.assertTemplateUsed(response, "catalog/literary_format_list.html")


class PrivateAuthorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first", "last_name": "Test last",
            "pseudonym": "Test Pseudonym",
        }
        self.client.post(reverse("catalog:author-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.pseudonym, form_data["pseudonym"])


# from django.test import TestCase
# from django.urls import reverse
# from .models import Item
#
#
# class SearchViewTest(TestCase):
#     def setUp(self):
#         # Создаём несколько объектов для поиска
#         Item.objects.create(name="Test Item 1")
#         Item.objects.create(name="Another Test Item")
#         Item.objects.create(name="Unrelated Item")
#
#     def test_search_results(self):
#         # Выполняем GET-запрос с параметром поиска
#         response = self.client.get(reverse('search_view'), {'query': 'Test'})
#
#         # Проверяем, что запрос успешен (статус 200)
#         self.assertEqual(response.status_code, 200)
#
#         # Проверяем, что вернулись нужные результаты
#         self.assertContains(response, "Test Item 1")
#         self.assertContains(response, "Another Test Item")
#         self.assertNotContains(response, "Unrelated Item")
#
#         # Проверяем, что шаблон использован правильно
#         self.assertTemplateUsed(response, 'search_results.html')
#
#         # Проверяем, что форма находится в контексте
#         self.assertIsInstance(response.context['form'], SearchForm)
#
#         # Проверяем, что результат поиска в контексте
#         self.assertEqual(len(response.context['results']), 2)
#
#     def test_empty_search_results(self):
#         # Тестируем случай, когда нет результатов
#         response = self.client.get(reverse('search_view'), {'query': 'Nonexistent'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['results']), 0)
