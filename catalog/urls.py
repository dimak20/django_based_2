from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.views import (
    index,
    LiteraryFormatListView,
    BookListView,
    AuthorListView,
    BookDetailView,
    test_session_view,
    LiteraryFormatCreateView,
    LiteraryFormatDeleteView,
    LiteraryFormatUpdateView,
    AuthorCreateView,
    AuthorDetailView,
    BookCreateView,
    BookUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("literary-formats/", LiteraryFormatListView.as_view(), name="literary-format-list"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("test-session/", test_session_view, name="test-session"),
    path("format/create/", LiteraryFormatCreateView.as_view(), name="format-create"),
    path("authors/create/", AuthorCreateView.as_view(), name="author-create"),
    path("format/<int:pk>/update/", LiteraryFormatUpdateView.as_view(), name="literary-format-update"),
    path("format/<int:pk>/delete/", LiteraryFormatDeleteView.as_view(), name="literary-format-delete"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "catalog"
