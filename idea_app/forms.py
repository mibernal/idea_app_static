from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'image', 'software_idea']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los widgets si es necesario
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control'})
        self.fields['image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        self.fields['software_idea'].widget = forms.Textarea(attrs={'class': 'form-control'})