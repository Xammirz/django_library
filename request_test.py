import requests, environ
env = environ.Env()
env.read_env()
key = env.str('API_KEY')
def aboba(request):
    
    author = request.GET.get('author', False)
    search = author if request.GET.get(
            'search', False) == "" else request.GET.get('search', False)
    queries = {'q': search, 'inauthor': author, 'key': key}
    r = requests.get(
            'https://www.googleapis.com/books/v1/volumes', params=queries)
    print(r)
    data = r.json()
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
if __name__ == '__main__':
    aboba()