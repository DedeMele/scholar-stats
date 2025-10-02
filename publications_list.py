from scholarly import scholarly
import json

AUTHOR_ID = "tMJF76UAAAAJ"

# Récupérer l'auteur
author = scholarly.search_author_id(AUTHOR_ID)
author = scholarly.fill(author, sections=['publications'])

publications_data = []

for pub in author['publications']:
    pub_filled = scholarly.fill(pub)
    title = pub_filled.get('bib', {}).get('title', "Sans titre")
    year = pub_filled.get('bib', {}).get('pub_year', "N/A")
    citations = pub_filled.get('num_citations', 0)
    
    publications_data.append({
        "title": title,
        "year": year,
        "citations": citations
    })

# Sauvegarde dans un JSON
with open("publications.json", "w", encoding="utf-8") as f:
    json.dump(publications_data, f, indent=2, ensure_ascii=False)

print("publications.json créé avec", len(publications_data), "publications.")
