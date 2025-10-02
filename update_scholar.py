#!/usr/bin/env python3
# update_scholar.py
# Script robuste pour récupérer les stats Google Scholar et écrire data.json
import os
import sys
import json
import traceback

try:
    from scholarly import scholarly
except Exception as e:
    print("ERREUR: impossible d'importer 'scholarly'. Installer la dépendance (pip install scholarly).")
    print(e)
    sys.exit(1)

AUTHOR_NAME = os.environ.get("AUTHOR_NAME", "David Mele")   # remplace via le workflow ou localement
AUTHOR_ID   = os.environ.get("AUTHOR_ID", "tMJF76UAAAAJ")         # optionnel : id Google Scholar (valeur user=xxxx dans l'URL)

def get_author_by_name(name, max_results=10):
    gen = scholarly.search_author(name)
    first = None
    for i in range(max_results):
        try:
            a = next(gen)
        except StopIteration:
            break
        if i == 0:
            first = a
        print(f"  -> résultat {i+1}: {a.get('name')}")
        if a.get('name','').strip().lower() == name.strip().lower():
            return a, True
    return (first, False) if first is not None else (None, False)

def main():
    try:
        print("Démarrage update_scholar.py")
        author = None
        exact = False

        if AUTHOR_ID:
            print(f"Essai via AUTHOR_ID = {AUTHOR_ID}")
            try:
                author = scholarly.search_author_id(AUTHOR_ID)
                exact = True
            except Exception as e:
                print("Impossible de récupérer via AUTHOR_ID :", e)
                author = None

        if author is None:
            print(f"Recherche par nom : '{AUTHOR_NAME}'")
            author, exact = get_author_by_name(AUTHOR_NAME)
            if author is None:
                print("Aucun résultat pour ce nom. Vérifie le nom exact tel qu'il apparaît sur Google Scholar.")
                sys.exit(2)
            if not exact:
                print("Attention : pas de correspondance exacte trouvée -> on prend le premier résultat trouvé.")

        print("Remplissage des données (cela peut prendre quelques secondes)...")
        author = scholarly.fill(author, sections=['indices', 'publications'])
        name = author.get("name", "")
        affiliation = author.get("affiliation", "")
        citations_total = author.get("citedby", 0)
        h_index = author.get("hindex", 0)
        publications_count = len(author.get("publications", []))
        cites_per_year = author.get("cites_per_year", {})

        # Trier les années
        years_sorted = sorted(cites_per_year.keys(), key=lambda y: int(y))
        years = [str(y) for y in years_sorted]
        citations = [cites_per_year[y] for y in years_sorted]

        data = {
            "name": name,
            "affiliation": affiliation,
            "citations_total": citations_total,
            "h_index": h_index,
            "years": years,
            "citations": citations,
            "publications_count": publications_count
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("data.json créé avec succès.")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception:
        print("ERREUR lors de l'exécution du script :")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

