"""Télécharge les données DVF géolocalisées (2021-2025)
pour les 12 départements de la région Auvergne-Rhône-Alpes."""
from pathlib import Path
import urllib.request

# Paramètres
DEPARTEMENTS = [
    "01",  # Ain
    "03",  # Allier
    "07",  # Ardèche
    "15",  # Cantal
    "26",  # Drôme
    "38",  # Isère
    "42",  # Loire
    "43",  # Haute-Loire
    "63",  # Puy-de-Dôme
    "69",  # Rhône (avec Lyon)
    "73",  # Savoie
    "74",  # Haute-Savoie
]
ANNEES = [2021, 2022, 2023, 2024, 2025]

URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/{annee}/departements/{dep}.csv.gz"
DOSSIER = Path(__file__).resolve().parent.parent / "data" / "raw"


def telecharger(dep, annee):
    """Télécharge un fichier (département + année) s'il n'existe pas déjà."""
    fichier = DOSSIER / f"dvf_{dep}_{annee}.csv.gz"
    if fichier.exists():
        print(f"Déjà présent : {fichier.name}")
        return True
    url = URL.format(annee=annee, dep=dep)
    try:
        urllib.request.urlretrieve(url, fichier)
        taille = fichier.stat().st_size / 1_000_000
        print(f"OK : {fichier.name} ({taille:.1f} Mo)")
        return True
    except Exception as e:
        if fichier.exists():
            fichier.unlink()  # supprime un fichier à moitié téléchargé
        print(f"Échec {dep} {annee} : {e}")
        return False


if __name__ == "__main__":
    DOSSIER.mkdir(parents=True, exist_ok=True)
    echecs = []
    for dep in DEPARTEMENTS:
        for annee in ANNEES:
            if not telecharger(dep, annee):
                echecs.append(f"{dep}-{annee}")

    total = len(DEPARTEMENTS) * len(ANNEES)
    print(f"\nTerminé : {total - len(echecs)}/{total} fichiers disponibles.")
    if echecs:
        print("Échecs :", ", ".join(echecs))