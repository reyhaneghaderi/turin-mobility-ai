import re
import unicodedata


def clean_text(text):

    # 1. Normalize Unicode
    text = unicodedata.normalize("NFKC", text)

    # 2. Replace non-breaking spaces
    text = text.replace("\xa0", " ")

    # 3. Split text into lines
    lines = text.splitlines()

    clean_lines = []

    # Lines coming from website interface
    unwanted_lines = [
        "Argomenti",
        "Tempo di lettura",
        "INDICE DELLA PAGINA",
        "Descrizione",
        "Link utili",
        "Contatta il comune",
        "Problemi in città",
        "Unità organizzativa responsabile",
        "Leggi le domande frequenti",
        "Richiedi assistenza",
        "Prenota appuntamento",
        "Segnala disservizio",
        "Valuta da 1 a 5 stelle la pagina",
        "Quanto sono chiare le informazioni su questa pagina?"
    ]

    for line in lines:

        # Remove spaces at beginning/end
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Remove unwanted website lines
        if line in unwanted_lines:
            continue

        # Remove website navigation
        if line.startswith("Home /"):
            continue

        # Remove reading-time lines
        # Example: 4 minuti
        if re.fullmatch(r"\d+\s+minuti", line):
            continue

        # Replace multiple spaces
        line = re.sub(r"\s+", " ", line)

        clean_lines.append(line)

    # Keep line structure
    text = "\n".join(clean_lines)

    return text.strip()