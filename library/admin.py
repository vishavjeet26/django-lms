from django.contrib import admin

# Register your models here.

from .models import Books, Author, Publisher, Student, Librarian, Issue

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('due_date', 'issue_date',)
# Register your models here.
admin.site.register(Books, BookAdmin)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(Issue)
