import spacy
import re

# Charger le modèle français
nlp = spacy.load("fr_core_news_md")

def clean_and_lemmatize(text):
    if not text:
        return ""

    # Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text.strip())

    # Utilisation de spaCy
    doc = nlp(text.lower())

    tokens = []
    for token in doc:
        # Suppression des stopwords, ponctuations, et tokens trop courts
        if token.is_stop or not token.is_alpha or len(token.text) <= 2:
            continue
        
        # token.is_stop : exclut articles, prépositions, pronoms fréquents
        # token.is_alpha : exclut chiffres, ponctuation, symboles

        # Lemmatisation
        lemma = token.lemma_

        # Suppression des apostrophes
        lemma = lemma.replace("’", "").replace("'", "")

        tokens.append(lemma)

    return " ".join(tokens)
