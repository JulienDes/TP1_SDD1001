from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Auteur import Auteur


class Livre:
    """
    Représente un livre avec son book_id, son titre, son auteur et s'il est disponible.

    Attributes:
        book_id (str): Le nom de l'auteur.
        titre (str): La nationalité de l'auteur.
        auteur (Auteur
        disponible (bool): Sa disponibilite
    """
    def __init__(self, book_id: str, titre: str, auteur: 'Auteur', disponible=True):
        from src.Auteur import Auteur

        if not isinstance(book_id, str):
            raise ValueError("Le book_id doit être une chaîne non vide")
        if not isinstance(titre, str):
            raise ValueError("Le titre doit être une chaîne non vide")
        if not isinstance(auteur, Auteur):
            raise ValueError("L'auteur doit être une instance de Auteur")

        self.book_id = book_id
        self.titre = titre
        self.auteur = auteur
        self.disponible = disponible

    def __str__(self):
        return f"Livre(id={self.book_id}, titre='{self.titre}', auteur='{self.auteur.nom}', disponible={self.disponible})"
