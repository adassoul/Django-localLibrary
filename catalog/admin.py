from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Language)

class BooksInline(admin.TabularInline): #(2)
    model = Book
    extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    #exclude = ['first_name']

    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline): #(2)
    model = BookInstance #(1)
    # extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline] #(2)
    
@admin.register(BookInstance) #(1)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ('id', 'display_title', 'borrower', 'status', 'due_back')
    
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, 
            {
                'fields': ('book', 'imprint', 'id')
            }
        ),
        ('Availability',
            {
                'fields': ('status', 'borrower', 'due_back')
            }              
        ),
    )
