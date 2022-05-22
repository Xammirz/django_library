from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from string import Template
import environ
from .forms import BookSearch
from django.views.generic import TemplateView
env = environ.Env()
env.read_env()  # reading .env file

key = env.str('API_KEY')
class HomePageView(TemplateView):
    template_name = 'index.html'

def index(request):
    form = BookSearch()
    return render(request, 'book_browse/index.html', {'form': form})


def books(request):

    author = request.GET.get('author', False)
    search = author if request.GET.get(
        'search', False) == "" else request.GET.get('search', False)

    if (search == False and author == False) or (search == "" and author == ""):
        return redirect('/')

    queries = {'q': search, 'inauthor': author, 'key': key}
    print(queries)
    r = requests.get(
        'https://www.googleapis.com/books/v1/volumes', params=queries)
    print(r)
    if r.status_code != 200:
        return render(request, 'book_browse/books.html', {'message': 'Извините, похоже, сейчас возникла проблема с Google Книгами.'})

    data = r.json()

    if not 'items' in data:
        return render(request, 'book_browse/books.html', {'message': 'Простите, такой книги не найдено.'})

    fetched_books = data['items']
    books = []
    for book in fetched_books:
        book_dict = {
            'title': book['volumeInfo'] ['title'],
            'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
            'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
            'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
            'info': book['volumeInfo']['infoLink'],
            'date': book['volumeInfo']['publishedDate'] if 'publishedDate' in book['volumeInfo'] else "",
            'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0
        }
        books.append(book_dict)
        print(books)
    def sort_by_pop(e):
        return e['popularity']

    books.sort(reverse=True, key=sort_by_pop)

    return render(request, 'book_browse/books.html', {'books': books})