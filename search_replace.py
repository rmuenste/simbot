import re 

def apply_translations(text, translations):
    """
    Perform a case-insensitive search and replace operation on the text.

    Parameters:
    - text (str): The input text to process.
    - translations (dict): A dictionary where keys are original words and values are translations.

    Returns:
    - str: The transformed text with translations applied.
    """
    def replace(match):
        # Get the matched word (case-insensitive match)
        original_word = match.group(0)
        # Find the translation for the original word, maintaining its case
        translation = translations[match.group(0).lower()]
        # Preserve original casing
        if original_word.isupper():
            return translation.upper()
        elif original_word.istitle():
            return translation.capitalize()
        else:
            return translation.lower()

    # Create a regex pattern to match all original words case-insensitively
    pattern = re.compile(r"|".join(re.escape(word) for word in translations.keys()), re.IGNORECASE)

    # Use the pattern to replace matches in the text
    return pattern.sub(replace, text)
