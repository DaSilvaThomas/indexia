def truncate_words(text):
    num_words=50

    words = text.split()

    if len(words) <= num_words:
        return text
    
    return " ".join(words[:num_words]) + "..."
