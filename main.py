import Bibliotheque, Auteur
from Emprunteur import Emprunteur


class Main:
    biblio = Bibliotheque.Bibliotheque()

    auteur = Auteur.Auteur('Julien', 'Canadien')
    biblio.ajouter_livre(book_id='1', titre="Amos daragon tome 1", auteur=auteur)
    biblio.ajouter_livre(book_id='2', titre="Amos daragon tome 2", auteur=auteur)

    auteur = Auteur.Auteur('Alex', 'Canadien')
    biblio.ajouter_livre(book_id='3', titre="La construction pour les nulls et ju", auteur=auteur)

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
        print(f"- {livre.titre}  (Auteur: {livre.auteur.nom}) ")

