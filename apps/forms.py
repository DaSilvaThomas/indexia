from django import forms
from .models import UploadedFile

class loginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur"
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre mot de passe"
        })
    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        labels = {
            'file': 'Choisir un fichier (txt, pdf et docx) :',
        }
        widgets = {
            'file': MultipleFileInput(attrs={
                'class': 'form-control',
                'id': 'file',
                'accept': '.txt,.pdf,.docx'
            }),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_extensions = ['.txt', '.pdf', '.docx']
        import os
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in allowed_extensions:
            raise forms.ValidationError("Seuls les fichiers .txt, .pdf et .docx sont autorisés.")

        return file
