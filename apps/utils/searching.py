import os
import difflib
from django.conf import settings
from apps.models import UploadedFile
from .indexing import load_index


INDEX_FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'inverted_index.json')


def search_documents(query):
    """
    Recherche des documents selon une requête.
    Retourne un tuple: (results, suggestions)
    """
    if not query:
        return UploadedFile.objects.none(), []

    index = load_index()
    query = query.lower().strip()

    # Détection des opérateurs booléens
    if ' and ' in query:
        terms = [t.strip() for t in query.split(' and ')]
        results = search_with_and(terms, index)
    elif ' or ' in query:
        terms = [t.strip() for t in query.split(' or ')]
        results = search_with_or(terms, index)
    else:
        results = search_single_term(query, index)

    # Si aucun résultat → proposer des suggestions
    suggestions = []
    if not results.exists():
        suggestions = suggest_similar_words(query, index)

    return results, suggestions


def search_single_term(term, index):
    """Recherche un seul terme"""    
    if term in index:
        file_ids = index[term]
        return UploadedFile.objects.filter(id__in=file_ids).order_by('-uploaded_at')
    return UploadedFile.objects.none()


def search_with_and(terms, index):
    """Recherche avec opérateur AND"""
    if not terms:
        return UploadedFile.objects.none()
    
    # Récupérer les ensembles de documents pour chaque terme
    sets = []
    for term in terms:
        if term in index:
            sets.append(set(index[term]))
        else:
            # Si un terme n'existe pas, l'intersection sera vide
            return UploadedFile.objects.none()
    
    # Intersection de tous les ensembles
    result_ids = sets[0]
    for s in sets[1:]:
        result_ids = result_ids.intersection(s)
    
    if result_ids:
        return UploadedFile.objects.filter(id__in=result_ids).order_by('-uploaded_at')
    return UploadedFile.objects.none()


def search_with_or(terms, index):
    """Recherche avec opérateur OR"""
    if not terms:
        return UploadedFile.objects.none()
    
    # Récupérer les ensembles de documents pour chaque terme
    result_ids = set()
    for term in terms:
        if term in index:
            result_ids.update(index[term])
    
    if result_ids:
        return UploadedFile.objects.filter(id__in=result_ids).order_by('-uploaded_at')
    return UploadedFile.objects.none()


def suggest_similar_words(query, index, limit=5):
    """Retourne les mots les plus proches du terme recherché."""
    if not query or not index:
        return []

    words = list(index.keys())

    # difflib utilise une similarité entre 0 et 1
    suggestions = difflib.get_close_matches(query, words, n=limit, cutoff=0.5)

    return suggestions