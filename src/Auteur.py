from src.Livre import Livre

class Auteur:
    """
    Représente un auteur avec son nom, sa nationalité et ses œuvres.

    Attributes:
        nom (str): Le nom de l'auteur.
        nationalite (str): La nationalité de l'auteur.
        oeuvres (List[Livre]): La liste des œuvres de l'auteur.
    """
    def __init__(self, nom: str, nationalite: str) -> None:
        if not isinstance(nom, str):
            raise ValueError("Le nom doit être une chaîne non vide")
        if not isinstance(nationalite, str):
            raise ValueError("La nationalité doit être une chaîne non vide")

        self.nom = nom
        self.nationalite = nationalite
        self.oeuvres = []


    def ajouter_oeuvre(self, livre: Livre) -> None:
        if not isinstance(livre, Livre):
            raise TypeError("l'oeuvre doit etre une instance de livre")
        self.oeuvres.append(livre)


    def __str__(self):
        return f"Auteur(nom='{self.nom}', nationalite='{self.nationalite}', oeuvres={len(self.oeuvres)})"