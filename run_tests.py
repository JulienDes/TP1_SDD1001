from tests.test_bibliotheque import TestBibliothequeMethods
import unittest

def run_tests():
    # Appel des tests unitaires.
    test_loader = unittest.TestLoader()  # Déclare une variable "Loader"
    test_suite = test_loader.loadTestsFromTestCase(TestBibliothequeMethods)  # Charge les tests
    test_runner = unittest.TextTestRunner()  # Déclare une variable "Runner"
    result = test_runner.run(test_suite)  # Exécute les tests chargés.

    # Sortie en fonction des résultats des tests
    if result.wasSuccessful():
        print("\nTous les tests ont réussi !")
    else:
        print(f"\nÉchec de {len(result.failures)} test(s).")

if __name__ == "__main__":
    run_tests()