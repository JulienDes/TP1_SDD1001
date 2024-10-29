from Auteur import Auteur
from Emprunteur import Emprunteur
from Livre import Livre

class Bibliotheque:

    def __init__(self):
        self.livres = {}
        self.auteurs = {}
        self.emprunteurs = {}


    def ajouter_livre(self, book_id: str, titre: str, auteur: Auteur):

        try:
            auteur_key = (auteur.nom, auteur.nationalite)

            # Si auteur_key n'existe pas ajout auteur dictionnaire
            if auteur_key not in self.auteurs:
                self.auteurs[auteur_key] = auteur

            # Si l'auteur existe on utilise l'instance
            else:
                auteur = self.auteurs[auteur_key]

            if book_id in self.livres:
                raise ValueError(f"Un livre avec l'ID {book_id} existe déjà.")

            # Creation nouveau livre
            nouveau_livre = Livre(book_id=book_id, titre=titre, auteur=auteur)

            # Ajout de l'oeuvre
            auteur.ajouter_oeuvre(nouveau_livre)

            self.livres[nouveau_livre.book_id] = nouveau_livre

        except Exception as e:
            print(f"Erreur lors de l'ajout du livre : {e}")
            raise


    def ajouter_emprunteur(self, emprunteur: Emprunteur):
        try:
            if not isinstance(emprunteur, Emprunteur) :
                raise TypeError(f"emprunteur: {emprunteur} doit etre une instance de Emprunteur")

            if emprunteur.emprunteur_id in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {emprunteur.emprunteur_id} existe deja.")

            self.emprunteurs[emprunteur.emprunteur_id] = emprunteur


        except Exception as e:
            print(f"Erreur lors de l'ajout de l'emprunteur : {e}")
            raise


    def rechercher_livre(self, recherche: str):
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

        try:
            if id_emprunteur not in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {id_emprunteur} n'existe pas.")

            if book_id not in self.livres:
                raise ValueError(f"book_id: {book_id} n'existe pas.")

            livre = self.livres[book_id]

            if not livre.disponible:
                raise ValueError(f"Le livre {livre.titre} n'est pas disponible")

            emprunteur = self.emprunteurs[id_emprunteur]

            emprunteur.livres_empruntes.append(livre)
            livre.disponible = False

        except Exception as e:
            print(f"Erreur lors de l'emprunt du livre : {e}")
            raise


    def retourner_livre(self, book_id: str, id_emprunteur: str):

        try:
            if id_emprunteur not in self.emprunteurs:
                raise ValueError(f"id_emprunteur: {id_emprunteur} n'existe pas.")

            if book_id not in self.livres:
                raise ValueError(f"book_id: {book_id} n'existe pas.")

            livre = self.livres[book_id]

            if livre.disponible:
                raise ValueError(f"Le livre {livre.titre} n'a pas ete emprunter")

            emprunteur = self.emprunteurs[id_emprunteur]
            emprunteur.livres_empruntes.remove(livre)
            livre.disponible = True

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