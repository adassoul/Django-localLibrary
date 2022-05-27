from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # the 'all()' is implied by default.
    num_authors = Author.objects.count()

    # books that contain "ro"
    num_book_ro = Book.objects.filter(title__icontains='ro').count()
    
    # genres that contain "ro"
    num_genre_ro = Genre.objects.filter(name__icontains='ro').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_book_ro' : num_book_ro,
        'num_genre_ro' : num_genre_ro,
        'number_of_visits' : num_visits, 
    }

    # Render the HTML template index.html with the date in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    # context_object_name = 'my_book_list' # changing name for list as a template var (generic was book_list)
    # (1) queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing title war
    #template_name = 'books/war_booksin_catalog_list.html' # Specify your own template name/location
    '''
    # (1) Override the class method that gets the query
    def get_queryset(self): 
        return Book.objects.filter(title__icontains='Le')[:5] 
    '''
    # Override the class method that makes the context dictionnary
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # 'Create any data and add it to the context'
        context['Authors'] = Author.objects.all()
        return context

class BookDetailView(generic.DetailView):
    model = Book    
    
class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBooksShownToLibrarianListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all the borrowed books and to whom."""
    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/all_borrowed_bookinstances_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back','borrower')