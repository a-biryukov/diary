from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic

from entries.forms import EntryForm
from entries.models import Entry
from entries.services import search_by_title_abd_text


class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entries:entry_list')

    def form_valid(self, form):
        if form.is_valid():
            entry = form.save()
            user = self.request.user
            entry.owner = user
        return super().form_valid(form)


class EntryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Entry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.owner.email:
            return self.object
        raise PermissionDenied


class EntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entries:entry_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.owner.email:
            return self.object
        raise PermissionDenied


class EntryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Entry
    success_url = reverse_lazy('entries:entry_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.owner.email:
            return self.object
        raise PermissionDenied


class EntryListView(LoginRequiredMixin, generic.ListView):
    model = Entry
    context_object_name = 'entries'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('query')
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        if query:
            queryset = search_by_title_abd_text(queryset, query, user).order_by('published_at').reverse()
        else:
            queryset = queryset.filter(owner=user).order_by('published_at').reverse()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['query'] = self.request.GET.get('query')
        return context_data
