import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Book, Author, BookInstance
from library.forms import RenewBookForm
from library.serializers import BookSerializer, AuthorSerializer


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(
                                status__exact="a").count()
    num_authors = Author.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        "index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            "num_visits": num_visits,
        },
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


# Create your views here.
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context["some_data"] = "This is just some data"
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "library/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).order_by(
            "due_back"
        )


@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.borrower = request.user
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("my-borrowed"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = (datetime.date.today() +
                                 datetime.timedelta(weeks=3))
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "library/book_renew_librarian.html", context)


class ArendView(generic.ListView):
    model = BookInstance
    template_name = "library/arend.html"


class AdminActionAuthorView(generic.ListView):
    model = Author
    template_name = "library/admin_action_author.html"


class AuthorCreate(CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {"date_of_death": "00/00/00"}


class AuthorUpdate(UpdateView):
    model = Author
    fields = (
        "__all__"
    )


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


class AdminActionBookView(generic.ListView):
    model = Book
    template_name = "library/admin_action_book.html"


class BookCreate(CreateView):
    model = Book
    fields = ["title", "summary", "isbn", "genre"]


class BookUpdate(UpdateView):
    model = Book
    fields = (
        "__all__"
    )


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("books")


class BookListViewAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


class BookDetailViewAPI(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorListViewAPI(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (AllowAny,)


class AuthorDetailViewAPI(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
