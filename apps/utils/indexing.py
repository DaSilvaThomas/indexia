import json
import os
from django.conf import settings


INDEX_FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'inverted_index.json')


def load_index():
    """Charge l'index inversé depuis le fichier JSON"""
    if os.path.exists(INDEX_FILE_PATH):
        try:
            with open(INDEX_FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_index(index):
    """Sauvegarde l'index inversé dans le fichier JSON"""
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    with open(INDEX_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def add_document_to_index(file_id, cleaned_text):
    """Ajoute un document à l'index inversé"""
    if not cleaned_text:
        return
    
    index = load_index()
    words = cleaned_text.split()
    
    # Pour chaque mot unique dans le document
    for word in set(words):
        if word not in index:
            index[word] = []
        
        # Ajouter l'ID du fichier s'il n'est pas déjà présent
        if file_id not in index[word]:
            index[word].append(file_id)
    
    save_index(index)


def remove_document_from_index(file_id):
    """Supprime un document de l'index inversé"""
    index = load_index()
    
    # Parcourir tous les mots et retirer l'ID du fichier
    for word in list(index.keys()):
        if file_id in index[word]:
            index[word].remove(file_id)
        
        # Supprimer le mot s'il n'a plus de documents associés
        if not index[word]:
            del index[word]
    
    save_index(index)
