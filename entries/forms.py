from django import forms

from entries.models import Entry


class EntryForm(forms.ModelForm):
    title = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={
        "class": "input-title",
        "type": "text1",
        "placeholder": "Заголовок"
    }))
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "input-text",
        "placeholder": "Напишите здесь что-нибудь..."
    }))

    class Meta:
        model = Entry
        fields = ('title', 'text',)
