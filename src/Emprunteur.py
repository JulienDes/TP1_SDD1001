
class Emprunteur:
    """
    Représente un emprunteur avec son nom, son id d'emprunter et sa liste de livre emprunter.

    Attributes:
        emprunteur_id (str): Le nom de l'auteur.
        nom (str): La nationalité de l'auteur.
        livres_empruntes ([Livre]): La liste des œuvres de l'auteur.
    """

    def __init__(self, emprunteur_id: str, nom: str):
        if not isinstance(emprunteur_id, str) or not emprunteur_id:
            raise ValueError("Le emprunteur_id doit être une chaîne non vide")
        if not isinstance(nom, str) or not nom:
            raise ValueError("Le nom doit être une chaîne non vide")

        self.emprunteur_id = emprunteur_id
        self.nom = nom
        self.livres_empruntes = []



    def __str__(self):
        return f"Emprunteur(id={self.emprunteur_id}, nom='{self.nom}', livres_empruntes={len(self.livres_empruntes)})"