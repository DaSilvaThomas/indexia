import os
from django.conf import settings
from apps.models import UploadedFile
from .indexing import load_index


INDEX_FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'inverted_index.json')


def search_documents(query):
    """
    Recherche des documents selon une requête avec opérateurs booléens
    Supporte AND, OR et les recherches simples
    """    
    if not query:
        return []
    
    index = load_index()
    query = query.lower().strip()
    
    # Détection des opérateurs booléens
    if ' and ' in query:
        terms = [t.strip() for t in query.split(' and ')]
        return search_with_and(terms, index)
    elif ' or ' in query:
        terms = [t.strip() for t in query.split(' or ')]
        return search_with_or(terms, index)
    else:
        # Recherche simple (un seul mot)
        return search_single_term(query, index)


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
