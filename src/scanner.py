from pathlib import Path
import json


FICHIER_MEMOIRE = Path(__file__).parent.parent / "data" / "fichiers.json"

# Taille maximale autorisée : 30 Mio
TAILLE_MAX = 30 * 1024 * 1024


def charger_memoire():
    if not FICHIER_MEMOIRE.exists():
        return {}

    with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def sauvegarder_memoire(memoire):
    FICHIER_MEMOIRE.parent.mkdir(parents=True, exist_ok=True)

    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as fichier:
        json.dump(memoire, fichier, indent=4, ensure_ascii=False)


def scanner_dossier(dossier):
    dossier = Path(dossier).expanduser()

    ancienne_memoire = charger_memoire()
    nouvelle_memoire = {}

    nouveaux = 0
    modifies = 0
    ignores = 0

    if not dossier.exists():
        print(f"Dossier introuvable : {dossier}")
        return

    print(f"\nAnalyse de : {dossier}\n")

    for fichier in dossier.rglob("*"):

        if not fichier.is_file():
            continue

        chemin = str(fichier)
        taille = fichier.stat().st_size

        # Ignorer les fichiers de plus de 30 Mio
        if taille > TAILLE_MAX:
            print(f"- Ignoré (> 30 Mio) : {chemin}")
            ignores += 1
            continue

        date_modification = fichier.stat().st_mtime

        nouvelle_memoire[chemin] = {
            "taille": taille,
            "date_modification": date_modification
        }

        # Nouveau fichier
        if chemin not in ancienne_memoire:
            print(f"+ Nouveau : {chemin}")
            nouveaux += 1

        # Fichier modifié
        elif ancienne_memoire[chemin] != nouvelle_memoire[chemin]:
            print(f"~ Modifié : {chemin}")
            modifies += 1

    sauvegarder_memoire(nouvelle_memoire)

    print("\n--- Résumé ---")
    print(f"Nouveaux fichiers : {nouveaux}")
    print(f"Fichiers modifiés : {modifies}")
    print(f"Fichiers ignorés : {ignores}")
    print("Scan terminé.")


if __name__ == "__main__":
    scanner_dossier("~/Téléchargements")