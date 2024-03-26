import spacy

def load_spacy_model(model_name):
    try:
        # Try loading the model
        nlp = spacy.load(model_name)
    except OSError:
        # If model doesn't exist, download and load it
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
    return nlp


def highlight_entities(text, entities):
    # Create a set to store the indices of characters that have been replaced
    replaced_indices = set()

    # Iterate over entities and replace each occurrence in the text
    for entity, label in entities:
        start_idx = 0
        while True:
            # Find the index of the entity in the text starting from the previous occurrence
            idx = text.find(entity, start_idx)
            if idx == -1:
                break
            
            # Check if the entity has already been replaced at this index
            if idx not in replaced_indices:
                font_label = "'Courier New', monospace;font-size: 12pt;"
                replacement = f'<span class="highlight">{entity} <span style="font-family: {font_label}">{label.upper()}</span></span>'               
                text = text[:idx] + replacement + text[idx + len(entity):]

                # Update start index to continue searching for next occurrence
                start_idx = idx + len(replacement)
                
                # Add replaced indices to set
                replaced_indices.update(range(idx, start_idx))
            else:
                # Move start index past the current entity
                start_idx = idx + len(entity)
    return text
