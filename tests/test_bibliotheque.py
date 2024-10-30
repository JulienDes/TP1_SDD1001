import unittest
from src.Auteur import Auteur
from src.Livre import Livre
from src.Bibliotheque import Bibliotheque
from src.Emprunteur import Emprunteur


class TestBibliothequeMethods(unittest.TestCase):
    def setUp(self):
        """ Initialise une nouvelle instance de Bibliotheque avant chaque test."""
        self.bibliotheque = Bibliotheque() # Crée une bibliothèque vide pour les tests


    def test_ajouter_livre(self):
        """
        Teste la méthode ajouter_livre en ajoutant un livre et en vérifiant son ajout correct.
            Etapes :
            1. Créer un auteur nommé 'Julien' de nationalité 'Canadien'.
            2. Ajouter un livre avec ID '1' intitulé "Amos daragon tome 1" par cet auteur.
            3. Récupérer le livre dans le dictionnaire de la bibliothèque et vérifier:
                - que le livre est bien présent (non None).
                - que le titre, le nom de l'auteur et la nationalité correspondent aux valeurs attendues.
        """
        auteur = Auteur('Julien', 'Canadien')   # Crée un auteur
        self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur)

        livre = self.bibliotheque.livres.get('1') # Récupère le livre ajouté
        self.assertIsNotNone(livre, "Le livre avec l'ID 1 n'a pas été ajouté.") # Vérifie que le livre existe

        # Vérifie que les détails du livre sont corrects
        self.assertEqual((livre.titre, livre.auteur.nom, livre.auteur.nationalite),
                         ("Amos daragon tome 1", "Julien", "Canadien"))


        with self.assertRaises(ValueError, msg=f"Un livre avec le meme ID '1' devrait declancher une erreur"):
            self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur)  # Livre déjà emprunté

    def test_ajouter_plusieurs_livres(self):
        """
        Teste la méthode ajouter_livre en ajoutant plusieurs livres et en vérifiant leur ajout et l'unicité par auteur.

        Étapes :
        1. Crée deux auteurs : 'Julien' 'Canadien' et 'Alexandre' 'Canadien'.
        2. Ajoute plusieurs livres avec des ID et titres différents pour les deux auteurs, y compris des titres en double pour tester l'unicité dans les oeuvres des auteurs.
        3. Pour chaque ID de livre ajouté, vérifie :
            - Que le livre n'est pas None, indiquant un ajout réussi.
            - Que le titre du livre, le nom et la nationalité de l'auteur sont corrects.
        4. Vérifie que les oeuvres des auteurs contiennent uniquement des livres uniques.
        """

        auteur1 = Auteur('Julien', 'Canadien')
        auteur2 = Auteur('Alexandre', 'Canadien')

        # Ajout des livres pour les deux auteurs, y compris des titres en double pour tester l'unicité
        self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)
        self.bibliotheque.ajouter_livre(book_id='2', titre="Amos daragon tome 1", auteur=auteur1)
        self.bibliotheque.ajouter_livre(book_id='3', titre="La construction pour les nulls", auteur=auteur1)
        self.bibliotheque.ajouter_livre(book_id='4', titre="La construction pour les nulls", auteur=auteur2)
        self.bibliotheque.ajouter_livre(book_id='5', titre="Amos daragon tome 1", auteur=auteur2)

        expected_books = {
            '1': ("Amos daragon tome 1", "Julien", "Canadien"),
            '2': ("Amos daragon tome 1", "Julien", "Canadien"),
            '3': ("La construction pour les nulls", "Julien", "Canadien"),
            '4': ("La construction pour les nulls", "Alexandre", "Canadien"),
            '5': ("Amos daragon tome 1", "Alexandre", "Canadien"),
        }

        # Validation
        for book_id, (titre, nom, nationalite) in expected_books.items():
            livre = self.bibliotheque.livres.get(book_id)
            self.assertIsNotNone(livre, f"Le livre avec l'ID {book_id} n'a pas été ajouté.")
            # Vérifie que les détails du livre sont corrects
            self.assertEqual((livre.titre, livre.auteur.nom, livre.auteur.nationalite),
                             (titre, nom, nationalite))

        expected_oeuvres = {
            ('Julien', 'Canadien'): ["Amos daragon tome 1", "La construction pour les nulls"],
            ('Alexandre', 'Canadien'): ["La construction pour les nulls", "Amos daragon tome 1"]
        }

        # Vérifie les oeuvres uniques pour chaque auteur, confirmant pas de doublons
        for (nom, nationalite), expected_books in expected_oeuvres.items():
            auteur_key = (nom, nationalite)
            self.assertIn(auteur_key, self.bibliotheque.auteurs,
                          f"L'auteur {auteur_key} n'est pas dans le dictionnaire.")

            oeuvres = [livre.titre for livre in self.bibliotheque.auteurs[auteur_key].oeuvres]

            # Vérifie que les oeuvres contiennent uniquement les titres uniques
            self.assertCountEqual(oeuvres, expected_books,
                                  f"Les oeuvres pour l'auteur {auteur_key} ne contiennent pas les titres uniques attendus.")

            # Confirme pas de doublons dans les oeuvres
            self.assertEqual(len(oeuvres), len(set(oeuvres)),
                             f"Les oeuvres pour l'auteur {auteur_key} contiennent des doublons.")

        with self.assertRaises(ValueError, msg=f"Un livre avec le meme ID '1' devrait declancher une erreur"):
            self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)  # Livre déjà emprunté


    def test_rechercher_livre(self):
        """ Teste la méthode rechercher_livre pour valider les résultats de recherche des livres. """
        auteur1 = Auteur('Julien', 'Canadien')
        self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)

        # Test pour une recherche qui devrait trouver le livre
        recherche = self.bibliotheque.rechercher_livre('ju')
        self.assertIsInstance(recherche, dict, "Le résultat de la recherche doit être un dictionnaire.")
        self.assertIn('1', recherche, "Le livre avec l'ID '1' devrait être trouvé dans la recherche.")
        self.assertEqual(recherche['1'].titre, "Amos daragon tome 1", "Le titre du livre trouvé devrait être correct.")
        self.assertEqual(recherche['1'].auteur.nom, "Julien",
                         "Le nom de l'auteur du livre trouvé devrait être correct.")

        # Test pour une recherche qui ne devrait pas trouver de livres
        with self.assertRaises(ValueError) as context:
            self.bibliotheque.rechercher_livre("Non Existant Book")


    def test_emprunter_livre(self):
        """ Teste la méthode emprunter_livre pour valider le processus d'emprunt de livres. """
        # Arrange : ajouter des livres et emprunteurs à la bibliothèque
        auteur = Auteur('Alex', 'Canadien')
        self.bibliotheque.ajouter_livre(book_id='4', titre="La construction pour les nulls et ju", auteur=auteur)
        self.bibliotheque.ajouter_livre(book_id='6', titre="Amos daragon tome 1", auteur=auteur)

        emprunteur = Emprunteur(emprunteur_id='1', nom='Luc')
        self.bibliotheque.ajouter_emprunteur(emprunteur)

        # Act : emprunter un livre
        self.bibliotheque.emprunter_livre('4', '1')

        # Assert : vérifier que le livre n'est plus disponible et que l'emprunteur l'a bien emprunté
        self.assertFalse(self.bibliotheque.livres['4'].disponible, "Le livre devrait être marqué comme non disponible.")
        self.assertIn(self.bibliotheque.livres['4'], self.bibliotheque.emprunteurs['1'].livres_empruntes,
                      "Le livre devrait être dans la liste des livres empruntés de l'emprunteur.")

        # Tester les cas d'erreurs
        with self.assertRaises(ValueError, msg="Un emprunteur inexistant devrait déclencher une erreur."):
            self.bibliotheque.emprunter_livre('4', '2')  # Emprunteur inexistant

        with self.assertRaises(ValueError, msg="Un livre inexistant devrait déclencher une erreur."):
            self.bibliotheque.emprunter_livre('10', '1')  # Livre inexistant

        with self.assertRaises(ValueError, msg="Un livre déjà emprunté devrait déclencher une erreur."):
            self.bibliotheque.emprunter_livre('4', '1')  # Livre déjà emprunté



    def test_retourner_livre(self):
        # Arrange : ajouter un livre emprunté et un emprunteur à la bibliothèque
        auteur = Auteur('Alex', 'Canadien')
        self.bibliotheque.ajouter_livre(book_id='4', titre="La construction pour les nulls et ju", auteur=auteur)

        emprunteur = Emprunteur(emprunteur_id='1', nom='Luc')
        self.bibliotheque.ajouter_emprunteur(emprunteur)

        # Emprunter le livre pour pouvoir le retourner ensuite
        self.bibliotheque.emprunter_livre('4', '1')

        # Act : retourner le livre
        self.bibliotheque.retourner_livre('4', '1')

        # Assert : vérifier que le livre est de nouveau disponible et retiré de la liste des livres empruntés
        self.assertTrue(self.bibliotheque.livres['4'].disponible,
                        "Le livre devrait être marqué comme disponible après le retour.")
        self.assertNotIn(self.bibliotheque.livres['4'], self.bibliotheque.emprunteurs['1'].livres_empruntes,
                         "Le livre ne devrait plus être dans la liste des livres empruntés de l'emprunteur après le retour.")

        # Tester les cas d'erreurs
        with self.assertRaises(ValueError, msg="Un emprunteur inexistant devrait déclencher une erreur."):
            self.bibliotheque.retourner_livre('4', '2')  # Emprunteur inexistant

        with self.assertRaises(ValueError, msg="Un livre inexistant devrait déclencher une erreur."):
            self.bibliotheque.retourner_livre('10', '1')  # Livre inexistant

        with self.assertRaises(ValueError,
                               msg="Retourner un livre qui n'a pas été emprunté devrait déclencher une erreur."):
            self.bibliotheque.retourner_livre('4', '1')  # Livre déjà retourné



if __name__ == "__main__":
    unittest.main()
