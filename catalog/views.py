from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import LiteraryFormatForm, AuthorCreationForm, BookForm, BookSearchForm
from .models import Book, Author, LiteraryFormat


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1
    }
    return render(request, "catalog/index.html", context=context)


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
