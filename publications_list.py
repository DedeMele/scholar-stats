from scholarly import scholarly
import json

AUTHOR_ID = "tMJF76UAAAAJ"

print("Récupération des publications de l'auteur", AUTHOR_ID)

# Récupération de l'auteur
author = scholarly.search_author_id(AUTHOR_ID)
author = scholarly.fill(author, sections=['publications'])

publications_data = []
biblio_lines = []

# Parcourir toutes les publications
for pub in author['publications']:
    pub_filled = scholarly.fill(pub)
    title = pub_filled.get('bib', {}).get('title', "Sans titre")
    year = pub_filled.get('bib', {}).get('pub_year', "N/A")
    citations = pub_filled.get('num_citations', 0)
    venue = pub_filled.get('bib', {}).get('venue', "Journal/Conference inconnu")
    authors = pub_filled.get('bib', {}).get('author', "Auteur(s) inconnu(s)")
    
    # Sauvegarde JSON
    publications_data.append({
        "title": title,
        "year": year,
        "citations": citations,
        "venue": venue,
        "authors": authors
    })
    
    # Format "scientifique"
    line = f"{authors} ({year}). {title}. *{venue}*. Citations: {citations}."
    biblio_lines.append(line)

# Sauvegarde JSON
with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(publications_data, f, indent=2, ensure_ascii=False)

# Sauvegarde version "références"
with open("publications.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(biblio_lines))
    

print(f"publications.json et publications.txt créés avec {len(publications_data)} publications.")
