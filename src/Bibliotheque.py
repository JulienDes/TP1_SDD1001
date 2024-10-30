from src.Auteur import Auteur
from src.Emprunteur import Emprunteur
from src.Livre import Livre

class Bibliotheque:
    """
    Classe représentant une bibliothèque qui gère des livres, des auteurs et des emprunteurs.

    Attributs:
        livres (dict): Dictionnaire des livres avec leur ID comme clé.
        auteurs (dict): Dictionnaire des auteurs avec une clé tuple (nom, nationalité).
        emprunteurs (dict): Dictionnaire des emprunteurs avec leur ID comme clé.
    """

    def __init__(self):
        """Initialise une nouvelle bibliothèque avec des dictionnaires vides pour les livres, les auteurs et les emprunteurs."""
        self.livres = {}
        self.auteurs = {}
        self.emprunteurs = {}


    def ajouter_livre(self, book_id: str, titre: str, auteur: Auteur):
        """
        Ajoute un livre à la bibliothèque.

        Args:
            book_id (str): L'identifiant unique du livre.
            titre (str): Le titre du livre.
            auteur (Auteur): L'auteur du livre.

        Raises:
            ValueError: Si le livre avec cet ID existe déjà.
        """

        try:
            # Vérifie si le livre existe déjà
            if book_id in self.livres:
                raise ValueError(f"Un livre avec l'ID {book_id} existe déjà.")

            auteur_key = (auteur.nom, auteur.nationalite)

            # Si auteur_key n'existe pas ajout auteur dictionnaire
            if auteur_key not in self.auteurs:
                self.auteurs[auteur_key] = auteur

            # Si l'auteur existe on utilise l'instance existante
            else:
                auteur = self.auteurs[auteur_key]

            # Creation nouveau livre
            nouveau_livre = Livre(book_id=book_id, titre=titre, auteur=auteur)

            # Vérifie si l'œuvre n'est pas déjà associée à l'auteur
            if not any(livre.titre == nouveau_livre.titre for livre in auteur.oeuvres):
                auteur.ajouter_oeuvre(nouveau_livre)    # Ajout de l'oeuvre

            # Ajout du livre à la bibliothèque
            self.livres[nouveau_livre.book_id] = nouveau_livre

        except Exception as e:
            print(f"Erreur lors de l'ajout du livre : {e}")
            raise


    def ajouter_emprunteur(self, emprunteur: Emprunteur):
        """
        Ajoute un emprunteur à la bibliothèque.

        Args:
            emprunteur (Emprunteur): L'emprunteur à ajouter.

        Raises:
            TypeError: Si l'objet n'est pas une instance d'Emprunteur.
            ValueError: Si l'ID de l'emprunteur existe déjà.
        """

        try:
            # Vérifie si l'emprunteur est une instance valide
            if not isinstance(emprunteur, Emprunteur) :
                raise TypeError(f"emprunteur: {emprunteur} doit etre une instance de Emprunteur")

            # Vérifie si l'emprunteur existe déjà
            if emprunteur.emprunteur_id in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {emprunteur.emprunteur_id} existe deja.")

            # Ajout de l'emprunteur au dictionnaire emprunteurs
            self.emprunteurs[emprunteur.emprunteur_id] = emprunteur


        except Exception as e:
            print(f"Erreur lors de l'ajout de l'emprunteur : {e}")
            raise


    def rechercher_livre(self, recherche: str):
        """
        Recherche des livres par titre ou par auteur. (ou inclusif)

        Args:
            recherche (str): Le critère de recherche (titre ou nom de l'auteur).

        Returns:
            dict: Un dictionnaire des livres correspondants à la recherche.

        Raises:
            ValueError: Si aucun livre n'est trouvé.
        """
        try:
            result = {
                id_: livre  for id_ , livre  in self.livres.items()
                if recherche.lower() in livre.titre.lower() or recherche.lower() in livre.auteur.nom.lower()
            }

            if not result:
                raise ValueError("Aucun livre n'est disponible")

            return result

        except Exception as e:
            print(f"Erreur lors de la recherche du livre : {e}")
            raise


    def emprunter_livre(self, book_id: str, id_emprunteur: str):
        """
        Permet à un emprunteur d'emprunter un livre.

        Args:
            book_id (str): L'identifiant du livre à emprunter.
            id_emprunteur (str): L'identifiant de l'emprunteur.

        Raises:
            ValueError: Si le livre ou l'emprunteur n'existe pas ou si le livre n'est pas disponible.
        """
        try:
            # Vérifie si l'emprunteur existe
            if id_emprunteur not in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {id_emprunteur} n'existe pas.")

            # Vérifie si le livre existe
            if book_id not in self.livres:
                raise ValueError(f"book_id: {book_id} n'existe pas.")

            livre = self.livres[book_id]

            # Vérifie la disponibilité du livre
            if not livre.disponible:
                raise ValueError(f"Le livre {livre.titre} n'est pas disponible")

            emprunteur = self.emprunteurs[id_emprunteur]

            emprunteur.livres_empruntes.append(livre)   # Ajoute le livre à la liste des livres empruntés
            livre.disponible = False    # Marque le livre comme non disponible

        except Exception as e:
            print(f"Erreur lors de l'emprunt du livre : {e}")
            raise


    def retourner_livre(self, book_id: str, id_emprunteur: str):
        """
        Permet à un emprunteur de retourner un livre.

        Args:
            book_id (str): L'identifiant du livre à retourner.
            id_emprunteur (str): L'identifiant de l'emprunteur.

        Raises:
            ValueError: Si le livre ou l'emprunteur n'existe pas ou si le livre n'a pas été emprunté.
        """
        try:
            # Vérifie si l'emprunteur existe
            if id_emprunteur not in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {id_emprunteur} n'existe pas.")

            # Vérifie si le livre existe
            if book_id not in self.livres:
                raise ValueError(f"book_id: {book_id} n'existe pas.")

            livre = self.livres[book_id]

            # Vérifie si le livre a été emprunté
            if livre.disponible:
                raise ValueError(f"Le livre {livre.titre} n'a pas ete emprunter")

            emprunteur = self.emprunteurs[id_emprunteur]
            emprunteur.livres_empruntes.remove(livre)   # Retire le livre de la liste des livres empruntés
            livre.disponible = True # Marque le livre comme disponible

        except Exception as e:
            print(f"Erreur lors du retour du livre : {e}")
            raise

    def print_info_console(self):
        # Afficher les livres et les auteurs
        print("Auteurs dans la bibliothèque:")
        for nom_auteur, auteur in self.auteurs.items():
            print(f"- {auteur.nom}")

        print("\nLivres dans la bibliothèque:")
        for book_id, livre in self.livres.items():
            print(f"- {livre.titre} (ID: {livre.book_id}) (DISPONIBLE: {livre.disponible}")

        # Afficher les œuvres de chaque auteur
        print("\nŒuvres de chaque auteur:")
        for nom_auteur, auteur in self.auteurs.items():
            print(f"Œuvres de {nom_auteur}:")
            for oeuvre in auteur.oeuvres:
                print(f"- {oeuvre.titre}")
            print()  # Ligne vide pour séparer les auteurs

        print("Emprunteur:")
        for emprunter_id, emprunteur in self.emprunteurs.items():
            print(f"- {emprunteur.nom} (ID: {emprunteur.emprunteur_id})")
            for livre in emprunteur.livres_empruntes:
                print(f"  * {livre.titre}")
        print('-------------------fin-------------------')