from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from collections import Counter
import os, json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

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

        if getattr(f, 'text_content', None):
            total_words_before += len(f.text_content.split())

        if getattr(f, 'cleaned_text', None):
            words = f.cleaned_text.split()
            total_words_after += len(words)
            all_cleaned_words.extend(words)

    # Mots supprimés
    words_removed = total_words_before - total_words_after

    # Statistiques sur le texte nettoyé
    unique_words = len(set(all_cleaned_words))
    most_common_words = Counter(all_cleaned_words).most_common(10)
    avg_words_per_file = total_words_after / total_files if total_files else 0

    # Données préparées pour Chart.js
    filetype_labels = list(filetype_counts.keys())
    filetype_values = list(filetype_counts.values())

    word_labels = [w for w, _ in most_common_words]
    word_values = [v for _, v in most_common_words]

    # Génération du nuage de mots (50 mots les plus fréquents)
    counter_50 = Counter(all_cleaned_words).most_common(50)
    freq_dict = dict(counter_50)

    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Blues',
        prefer_horizontal=1.0,
        max_words=50,
        random_state=42
    ).generate_from_frequencies(freq_dict)

    # Convertir en image Base64 pour afficher dans le template
    img_buffer = io.BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

    context = {
        'total_files': total_files,
        'total_words_before': total_words_before,
        'total_words_after': total_words_after,
        'words_removed': words_removed,
        'unique_words': unique_words,
        'avg_words_per_file': round(avg_words_per_file, 2),
        'filetype_labels': json.dumps(filetype_labels),
        'filetype_values': json.dumps(filetype_values),
        'word_labels': json.dumps(word_labels),
        'word_values': json.dumps(word_values),
        'wordcloud_image': img_base64,
    }

    return render(request, 'apps/statistic.html', context)
