from django.test import TestCase

from catalog.forms import AuthorCreationForm


class FormsTests(TestCase):
    def test_author_creation_form_with_pseudonym_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first", "last_name": "Test last",
            "pseudonym": "Test Pseudonym",
        }
        form = AuthorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


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
