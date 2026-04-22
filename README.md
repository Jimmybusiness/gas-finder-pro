# ⛽ Essence Pas Chère (Gas Finder Pro)

Application mobile-first pour trouver les stations-service les moins chères autour de vous en France.

## Fonctionnalités

- **Géolocalisation GPS** : Détecte automatiquement votre position
- **Tous les carburants** : Gazole, SP95, SP95-E10, SP98, E85, GPLc
- **Rayon personnalisable** : De 1 à 50 km autour de vous
- **Tri par prix** : Les stations les moins chères en premier
- **Itinéraire Google Maps** : Navigation directe vers la station choisie
- **Design iOS-like** : Interface moderne et épurée, optimisée mobile

## Source de données

Données officielles du gouvernement français en temps réel :
[Prix des carburants en France - data.economie.gouv.fr](https://data.economie.gouv.fr)

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technologies

- Python 3.10+
- Streamlit
- API Open Data du gouvernement français
- Streamlit Geolocation

## Licence

MIT