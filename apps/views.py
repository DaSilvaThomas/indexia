from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from collections import Counter
import os
import json

from .forms import UploadFileForm, loginForm
from .models import UploadedFile

from .utils.text_extraction import extract_text_from_file
from .utils.text_cleaning import clean_and_lemmatize


def login_view(request):
     form = loginForm(request.POST or None)

     if request.method == 'POST' and form.is_valid():
          username = form.cleaned_data['username']
          password = form.cleaned_data['password']
          user = authenticate(request, username=username, password=password)
          
          if user is not None and user.is_superuser:
               login(request, user)
               return redirect('home')
          else:
               messages.error(request, "Identifiants invalides ou non autorisé.")
     
     return render(request, 'apps/login.html', {
          'form': form,
          'breadcrumbs': [
               ("Accueil", "/"),
               ("Connexion", "/connexion/")
          ]
     })


def logout_view(request):
     logout(request)
     return redirect('home')


def home_view(request):
     pass

     return render(request, 'apps/home.html', {
          'breadcrumbs': [("Accueil", "/")],
     })


@login_required
def upload_view(request):
     if request.method == 'POST':
          form = UploadFileForm(request.POST, request.FILES)

          files = request.FILES.getlist('file')

          if files:
               for f in files:
                    uploaded_file = UploadedFile.objects.create(file=f)
                    file_path = uploaded_file.file.path

                    text = extract_text_from_file(file_path)
                    uploaded_file.text_content = text

                    cleaned = clean_and_lemmatize(text)
                    uploaded_file.cleaned_text = cleaned

                    uploaded_file.save()

               return redirect('document')
          else:
               form.add_error('file', "Veuillez sélectionner au moins un fichier.")
     else:
          form = UploadFileForm()

     return render(request, 'apps/upload.html', {
          'form': form,
          'breadcrumbs': [
               ("Accueil", "/"),
               ("Importer", "/importer/")
          ]
     })


@login_required
def delete_file_view(request, pk):
    file_obj = get_object_or_404(UploadedFile, pk=pk)
    
    if file_obj.file:
          file_path = file_obj.file.path
          if os.path.exists(file_path):
               os.remove(file_path)
    
    file_obj.delete()
    
    return redirect('document')


@login_required
def delete_all_files_view(request):
     files = UploadedFile.objects.all()
     
     for f in files:
          if f.file:
               file_path = f.file.path
               if os.path.exists(file_path):
                    os.remove(file_path)
     
     files.delete()
     
     return redirect('document')


@login_required
def document_view(request):
     files_list = UploadedFile.objects.all().order_by('-uploaded_at')
     paginator = Paginator(files_list, 12)

     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)

     return render(request, 'apps/document.html', {
          'page_obj': page_obj,
          'breadcrumbs': [
               ("Accueil", "/"),
               ("Documents", "/documents/")
          ]
     })


@login_required
def statistic_view(request):
     files = UploadedFile.objects.all()

     total_files = files.count()
     total_words_before = 0
     total_words_after = 0
     all_cleaned_words = []

     filetype_counts = Counter()

     for f in files:
          # Compte par type de fichier
          ext = os.path.splitext(f.file.name)[1].lower()
          filetype_counts[ext] += 1

          if f.text_content:
               total_words_before += len(f.text_content.split())

          if f.cleaned_text:
               words = f.cleaned_text.split()
               total_words_after += len(words)
               all_cleaned_words.extend(words)

     # Mots supprimés
     words_removed = total_words_before - total_words_after

     # Statistiques sur le texte nettoyé
     unique_words = len(set(all_cleaned_words))
     most_common_words = Counter(all_cleaned_words).most_common(10)
     avg_words_per_file = total_words_after / total_files if total_files else 0

     context = {
          'total_files': total_files,
          'total_words_before': total_words_before,
          'total_words_after': total_words_after,
          'words_removed': words_removed,
          'unique_words': unique_words,
          'avg_words_per_file': round(avg_words_per_file, 2),
          'filetype_counts': dict(filetype_counts),
          'most_common_words': most_common_words,
     }

     return render(request, 'apps/statistiques.html', context)
