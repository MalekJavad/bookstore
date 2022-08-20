from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 4


# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'

@login_required()
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_comments = book.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment_form = comment_form.save(commit=False)
            new_comment_form.book = book
            new_comment_form.user = request.user
            new_comment_form.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'book': book,
        'comments': book_comments,
        'comment_form': comment_form
    }
    return render(request, 'books/book_detail.html', context)


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ('title', 'author', 'description', 'price', 'cover', )
    template_name = 'books/book_create.html'


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ('title', 'author', 'description', 'price', 'cover', )
    template_name = 'books/book_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user



