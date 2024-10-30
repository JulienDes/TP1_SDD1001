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
                - Que le livre est bien présent (non None).
                - Que le titre, le nom de l'auteur et la nationalité correspondent aux valeurs attendues.

        Raises:
            ValueError: Si le livre ajoute a la bibliotheque a le meme id qu'un livre deja present.
        """

        auteur = Auteur('Julien', 'Canadien')   # Crée un auteur
        self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur)

        livre = self.bibliotheque.livres.get('1') # Récupère le livre ajouté
        self.assertIsNotNone(livre, "Le livre avec l'ID 1 n'a pas été ajouté.") # Vérifie que le livre existe

        # Vérifie que les détails du livre sont corrects
        self.assertEqual((livre.titre, livre.auteur.nom, livre.auteur.nationalite),
                         ("Amos daragon tome 1", "Julien", "Canadien"))

        # Vérifie les cas d'erreur attendus
        with self.assertRaises(ValueError, msg=f"Un livre avec le meme ID '1' devrait declancher une erreur"):
            self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur)  # Livre avec le meme id deja la

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

        Raises:
            ValueError: Si le livre ajoute a la bibliotheque a le meme id qu'un livre deja present.
        """

        auteur1 = Auteur('Julien', 'Canadien')
        auteur2 = Auteur('Alexandre', 'Canadien')

        # Ajout des livres pour les deux auteurs, y compris des titres en double pour tester l'unicité des oeuvres des auteurs
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

        # Validation de l'ajout des livres
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

        # Vérifie les cas d'erreur attendus
        with self.assertRaises(ValueError, msg=f"Un livre avec le meme ID '1' devrait declancher une erreur"):
            self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)  # Livre déjà ajoute

    def test_rechercher_livre(self):
        """
        Teste la méthode rechercher_livre pour valider les résultats de recherche de livres.

        Étapes :
        1. Crée un auteur 'Julien' de nationalité 'Canadien'.
        2. Ajoute un livre avec ID '1' intitulé "Amos daragon tome 1" pour cet auteur dans la bibliothèque.
        3. Effectue une recherche en utilisant un terme partiel ('ju') et vérifie :
            - Que le résultat est un dictionnaire contenant le livre correspondant.
            - Que le titre et le nom de l'auteur dans le résultat sont corrects.
        4. Teste une recherche avec un titre inexistant pour s'assurer que l'exception ValueError est levée.

        Vérifications :
        - Que le résultat de la recherche soit un dictionnaire.
        - Que l'ID du livre ajouté ('1') soit présent dans les résultats.
        - Que le titre et l'auteur correspondent aux informations du livre ajouté.
        - Que rechercher un livre inexistant déclenche une erreur.

        Raises:
            ValueError: Si la recherche ne trouve pas de livre.
        """

        auteur1 = Auteur('Julien', 'Canadien')
        auteur2 = Auteur('Alexandre', 'Canadien')
        self.bibliotheque.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)
        self.bibliotheque.ajouter_livre(book_id='2', titre="Travaillier avec Julien", auteur=auteur2)
        self.bibliotheque.ajouter_livre(book_id='3', titre="La construction pour les nulls", auteur=auteur2)

        # Test pour une recherche qui devrait trouver le livre
        recherche = self.bibliotheque.rechercher_livre('ju')
        self.assertIsInstance(recherche, dict, "Le résultat de la recherche doit être un dictionnaire.")
        self.assertIn('1', recherche, "Le livre avec l'ID '1' devrait être trouvé dans la recherche.")
        self.assertIn('2', recherche, "Le livre avec l'ID '2' devrait être trouvé dans la recherche.")
        self.assertEqual(recherche['1'].titre, "Amos daragon tome 1", "Le titre du livre trouvé devrait être correct.")
        self.assertEqual(recherche['2'].titre, "Travaillier avec Julien", "Le titre du livre trouvé devrait être correct.")
        self.assertNotIn('3', recherche, "Le livre avec l'ID '3' ne devrait pas être trouvé dans la recherche.")

        self.assertEqual(recherche['1'].auteur.nom, "Julien",
                         "Le nom de l'auteur du livre trouvé devrait être correct.")

        self.assertEqual(recherche['2'].auteur.nom, "Alexandre",
                         "Le nom de l'auteur du livre trouvé devrait être correct.")

        # Test pour une recherche qui ne devrait pas trouver de livres
        with self.assertRaises(ValueError) as context:
            self.bibliotheque.rechercher_livre("Non Existant Book")


    def test_emprunter_livre(self):
        """
        Teste la méthode emprunter_livre pour valider le processus d'emprunt de livres.

        Ce test vérifie le comportement de l'emprunt de livres dans la bibliothèque, en s'assurant que :
            - Un livre peut être emprunté par un emprunteur
            - Le livre devient indisponible après avoir été emprunté
            - Le livre est ajouté à la liste des livres empruntés de l'emprunteur

        Le test couvre également les cas d'erreur suivants :
            - Emprunt par un emprunteur inexistant
            - Emprunt d'un livre inexistant
            - Emprunt d'un livre déjà emprunté

        Raises:
            ValueError: Si l'emprunteur ou le livre n'existent pas, ou si le livre est déjà emprunté.
        """

        # Création d'un auteur
        auteur = Auteur('Alex', 'Canadien')

        # Ajout de livres à la bibliothèque
        self.bibliotheque.ajouter_livre(book_id='4', titre="La construction pour les nulls et ju", auteur=auteur)
        self.bibliotheque.ajouter_livre(book_id='6', titre="Amos daragon tome 1", auteur=auteur)

        # Création et ajout d'un emprunteur à la bibliothèque
        emprunteur = Emprunteur(emprunteur_id='1', nom='Luc')
        self.bibliotheque.ajouter_emprunteur(emprunteur)

        # L'emprunteur 'Luc', id '1' emprunte le livre avec l'ID '4'
        self.bibliotheque.emprunter_livre('4', '1')

        # Vérification que l'emprunteur est bien ajouté dans la liste des emprunteurs de la bibliothèque
        self.assertIn(
            '1',
            self.bibliotheque.emprunteurs,
            "L'emprunteur devrait être dans la liste des emprunteurs de la bibliothèque."
        )

        # Vérification que le livre est marqué comme indisponible apres l'emprunt
        self.assertFalse(self.bibliotheque.livres['4'].disponible, "Le livre devrait être marqué comme non disponible.")

        # Vérification que le livre est dans la liste des livres empruntés par l'emprunteur
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
        """
        Teste la fonctionnalité de retour d'un livre dans la bibliothèque.

        Ce test vérifie le bon fonctionnement du processus de retour d'un livre emprunté,
        en s'assurant que le livre redevient disponible et que l'emprunteur n'a plus le livre
        dans sa liste de livres empruntés. Il couvre également les cas d'erreurs suivants :
            - Retour par un emprunteur inexistant
            - Retour d'un livre inexistant
            - Retour d'un livre qui n'a pas été emprunté

        Raises:
            ValueError: Si l'emprunteur ou le livre n'existent pas, ou si le livre n'est pas emprunté.
        """

        # Arrange : ajouter un livre emprunté et un emprunteur à la bibliothèque
        auteur = Auteur('Alex', 'Canadien')
        self.bibliotheque.ajouter_livre(book_id='4', titre="La construction pour les nulls et ju", auteur=auteur)

        emprunteur = Emprunteur(emprunteur_id='1', nom='Luc')
        self.bibliotheque.ajouter_emprunteur(emprunteur)

        # Emprunter le livre pour pouvoir le retourner ensuite
        self.bibliotheque.emprunter_livre('4', '1')

        # Retourner le livre
        self.bibliotheque.retourner_livre('4', '1')

        # Vérifier que le livre est de nouveau disponible
        self.assertTrue(self.bibliotheque.livres['4'].disponible,
                        "Le livre devrait être marqué comme disponible après le retour.")

        # Vérifier que le livre n'est plus dans la liste des livres empruntés de l'emprunteur
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
