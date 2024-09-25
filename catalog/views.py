from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import LiteraryFormatForm, AuthorCreationForm, BookForm, BookSearchForm
from .models import Book, Author, LiteraryFormat


@login_required
def index(request: HttpRequest) -> HttpResponse:
    book_list = Book.objects.all()
    sort_by = request.GET.get('sort_by')  # Укажите колонку по умолчанию
    if sort_by:
        sort_dir = request.GET.get('sort_dir', 'asc')  # Направление сортировки
        # Проверяем направление сортировки и составляем аргумент для order_by
        if sort_dir == 'desc':
            sort_by = f'-{sort_by}'
            book_list = book_list.order_by(sort_by)
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        book_list = book_list.filter(title__icontains=form.cleaned_data["title"])
    book_format = request.GET.get("format")
    if book_format:
        book_list = book_list.filter(format__name=book_format)
    paginate_by_str = request.GET.get("paginate_by", "5")
    try:
        paginate_by = int(paginate_by_str)
    except ValueError:
        paginate_by = 5
    paginator = Paginator(book_list, paginate_by)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    books = paginator.get_page(page_number)
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1,
        "book_list_raw": book_list,
        "form": form,
        "page_obj": page_obj,
        "paginate_by": paginate_by,
        "book_list_list": page_obj.object_list,
        "book_list": books,
        "current_sort_by": request.GET.get('sort_by', 'default_column'),
        "current_sort_dir": request.GET.get('sort_dir', 'asc')
    }
    return render(request, "catalog/index.html", context=context)

@login_required
def index2(request: HttpRequest) -> HttpResponse:
    book_list = Book.objects.all()

    # Используем сохранённые параметры из сессии, если они есть
    search_query = request.session.get('search', '')
    sort_by = request.session.get('sort_by', '')  # Укажите колонку по умолчанию
    sort_dir = request.session.get('sort_dir', 'asc')  # Направление сортировки
    paginate_by_str = request.session.get("paginate_by", "5")
    page_number = request.GET.get("page")  # Из запроса

    # Если передан поисковый запрос, фильтруем
    if search_query:
        book_list = book_list.filter(title__icontains=search_query)

    # Обработка сортировки
    if sort_by:
        if sort_dir == 'desc':
            sort_by = f'-{sort_by}'
        book_list = book_list.order_by(sort_by)

    # Обработка пагинации
    try:
        paginate_by = int(paginate_by_str)
    except ValueError:
        paginate_by = 5
    paginator = Paginator(book_list, paginate_by)
    page_obj = paginator.get_page(page_number)

    # Остальные параметры
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1,
        "form": BookSearchForm(initial={'title': search_query}),  # Передаем поисковый запрос в форму
        "page_obj": page_obj,
        "paginate_by": paginate_by,
        "book_list": page_obj.object_list,
        "is_paginated": False,
        "current_sort_by": sort_by,
        "current_sort_dir": sort_dir
    }
    return render(request, "catalog/index.html", context=context)


@login_required
def BookChangeView(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    book.boolean = not book.boolean
    book.save()
    return redirect("catalog:index")

@login_required
def BookChangeView2(request, pk: int):
    book = get_object_or_404(Book, pk=pk)

    # Сохраняем параметры поиска и пагинации в сессии
    if request.GET.get('search'):
        request.session['search'] = request.GET['search']
    if request.GET.get('sort_by'):
        request.session['sort_by'] = request.GET['sort_by']
    if request.GET.get('sort_dir'):
        request.session['sort_dir'] = request.GET['sort_dir']
    if request.GET.get('page'):
        request.session['page'] = request.GET['page']
    if request.GET.get('paginate_by'):
        request.session['paginate_by'] = request.GET['paginate_by']

    # Изменяем состояние книги
    book.boolean = not book.boolean
    book.save()

    # Перенаправляем на страницу индекса с параметрами
    return redirect("catalog:index")


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_format_list"
    # queryset = LiteraryFormat.objects.filter(name__endswith="y")


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list'
    paginate_by = 2
    # queryset = Book.objects.select_related("format")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = BookSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm


def test_session_view(request: HttpRequest) -> HttpResponse:
    request.session["book"] = "Test session book"
    return HttpResponse(
        "<h1>Test Session</h1>"
        f"<h4>Session data: {request.session['book']}</h4>"
    )


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = LiteraryFormatForm
    success_url = reverse_lazy("catalog:literary-format-list")
    template_name = "catalog/format_form.html"
    # model = LiteraryFormat
    # fields = "__all__"


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-format-list")
    template_name = "catalog/format_form.html"


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    template_name = "catalog/format_confirm_delete.html"
    success_url = reverse_lazy("catalog:literary-format-list")


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = AuthorCreationForm
    model = Author
    success_url = reverse_lazy("catalog:author-list")


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm



    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["lot_id"] = self.request.POST.get("lot_id")
    #     return kwargs


# class PersonForm(forms.ModelForm):
#     MIN_BIRTH_YEAR = 1900
#     birth_year = forms.IntegerField(
#         required=True,
#         validators=[MinValueValidator(MIN_BIRTH_YEAR)]
#     )
#     class Meta:
#         model = Person
#         fields = ("full_name", "birth_year", "hobby", )


# class DriverUpdateLicenseView(LoginRequiredMixin, generic.UpdateView):
#     model = Driver
#     form_class = DriverLicenseUpdateForm
#     template_name = "taxi/driver_form.html"
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
#
# class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Driver
#     success_url = reverse_lazy("taxi:driver-list")
#
#
# class AddOrRemoveCar(LoginRequiredMixin, View):
#     def post(self, request, pk, action):
#         driver = request.user
#         car = get_object_or_404(Car, pk=pk)
#         if action == "add":
#             driver.cars.add(car)
#         if action == "remove":
#             driver.cars.remove(car)
#         return redirect("taxi:car-detail", pk=pk)


# class AddOrRemoveCar(LoginRequiredMixin, View):
#     def post(self, request, pk, action):
#         driver = request.user
#         car = get_object_or_404(Car, pk=pk)
#         if action == "add":
#             driver.cars.add(car)
#         if action == "remove":
#             driver.cars.remove(car)
#         return redirect("taxi:car-detail", pk=pk)

# class AddOrRemoveCar(LoginRequiredMixin, View):
#     def post(self, request, **kwargs):
#         driver = request.user
#         car = get_object_or_404(Car, pk=self.kwargs.get("pk"))
#         action = self.kwargs.get("action")
#         if action == "add":
#             driver.cars.add(car)
#         elif action == "remove":
#             driver.cars.remove(car)
#         return redirect("taxi:car-detail", pk=self.kwargs.get("pk"))











# def book_create_view(request: HttpRequest) -> HttpResponse:
    # if request.method == "GET":
    #     context = {
    #         "form": LiteraryFormatForm()
    #     }
    #     return render(request, "catalog/format_form.html", context=context)
    # elif request.method == "POST":
    #     form = LiteraryFormatForm(request.POST)
    #     if form.is_valid():
    #         LiteraryFormat.objects.create(**form.cleaned_data)
    #         return HttpResponseRedirect(reverse("catalog:literary-format-list"))
    #     context = {
    #         "form": form
    #     }
    #     return render(request, "catalog/format_form.html", context=context)
    # context = {}
    # form = LiteraryFormatForm(request.POST or None)
    # if form.is_valid():
    #     form.save()
    #     return HttpResponseRedirect(reverse("catalog:literary-format-list"))
    # context["form"] = form
    # return render(request, "catalog/format_form.html", context=context)



# def book_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
#     try:
#         book = Book.objects.select_related("format").get(id=pk)
#     except Book.DoesNotExist:
#         raise Http404("Does not exist")
#     context = {
#         "book": book,
#     }
#     return render(request, "catalog/book_detail.html", context=context)


# def literary_format_list_view(request: HttpRequest) -> HttpResponse:
#     literary_format_list = LiteraryFormat.objects.all()
#     context = {
#         "literary_format_list": literary_format_list
#     }
#     return render(request, "catalog/literary_format_list.html", context=context)


# def hello_world1(request: HttpRequest, unique_number) -> HttpResponse:
#     print(f"Request params: {request.GET}")
#     return HttpResponse(
#         "<html>"
#         "<h1>Hello, world!</h1>"
#         f"<h4>Unique number: {unique_number}</h4>"
#         "</html>"
#     )

#
# def index(request) -> HttpResponse:
#     all = Movie.objects.all()
#     paginate_by_str = request.GET.get("paginate_by", "5")
#     try:
#         paginate_by = int(paginate_by_str)
#     except ValueError:
#         paginate_by = 5
#     paginator = Paginator(all, paginate_by)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         "page_obj": page_obj,
#         "paginate_by": paginate_by,
#         "post_list": page_obj.object_list,
#     }
#     return render(request, "movies/index.html", context=context)
