import json
from scholarly import scholarly

author_name = "David Mele"

# Recherche du profil
search_query = scholarly.search_author(author_name)
author = next(search_query)

# Remplissage des données (citations + publications)
author = scholarly.fill(author, sections=['indices', 'publications'])

# Récupération des infos principales
citations_total = author['citedby']
h_index = author['hindex']
citations_per_year = author.get("cites_per_year", {})

# Organisation des données
data = {
    "name": author["name"],
    "affiliation": author.get("affiliation", ""),
    "citations_total": citations_total,
    "h_index": h_index,
    "years": list(citations_per_year.keys()),
    "citations": list(citations_per_year.values()),
    "publications_count": len(author["publications"])
}

# Sauvegarde dans un fichier JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Données exportées dans data.json")
