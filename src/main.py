from src.Livre import Livre
from src.Emprunteur import Emprunteur
from src.Auteur import Auteur
from src.Bibliotheque import Bibliotheque


class Main:
    biblio = Bibliotheque()

    auteur1 = Auteur('Julien', 'Canadien')
    biblio.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur1)
    biblio.ajouter_livre(book_id='2', titre="Amos daragon tome 2", auteur=auteur1)
    biblio.ajouter_livre(book_id='3', titre="Amos daragon tome 1", auteur=auteur1)

    auteur2 = Auteur('Alex', 'Canadien')
    biblio.ajouter_livre(book_id='4', titre="La construction pour les nulls et ju", auteur=auteur2)
    biblio.ajouter_livre(book_id='5', titre="La construction pour les nulls et ju", auteur=auteur2)
    biblio.ajouter_livre(book_id='6', titre="Amos daragon tome 1", auteur=auteur2)

    emprunter1 = Emprunteur(emprunteur_id='1', nom='Luc')
    emprunter2 = Emprunteur(emprunteur_id='2', nom='Charles')
    biblio.ajouter_emprunteur(emprunter1)
    biblio.ajouter_emprunteur(emprunter2)

    biblio.emprunter_livre('1', '1')
    biblio.emprunter_livre('3', '2')

    biblio.print_info_console()

    biblio.retourner_livre('3', '2')
    biblio.print_info_console()

    recherche = biblio.rechercher_livre('ju')

    for i, livre in recherche.items():
        print(f"- ({livre.book_id}) {livre.titre}  (Auteur: {livre.auteur.nom}) ")

