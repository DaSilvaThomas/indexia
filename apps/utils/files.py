import os

ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}

def is_allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def filter_allowed_files(files):
    """Filtre une liste de fichiers pour ne garder que ceux autorisés"""
    return [f for f in files if is_allowed_file(f.name)]
