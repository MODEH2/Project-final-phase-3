from argparse import ArgumentParser
from datetime import date
from sys import argv
import datetime as dt
import requests

def analyse_de_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")

    parser.add_argument("-d", "--debut", 
                        type=str,
                        metavar="DATE", 
                        help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f", "--fin", 
                        type=str,
                        metavar="DATE", 
                        help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
    parser.add_argument("-v", "--valeur", 
                        metavar="{fermeture,ouverture,min,max,volume}", 
                        default="fermeture",
                        help="La valeur désirée (par défaut: fermeture)")
    parser.add_argument("symbole", 
                        type=str,
                        nargs="+",
                        help="Nom d'un symbole boursier")

    return parser.parse_args()


def produire_historique(symbole: str = "AAPL", debut: date = None, fin: date = None, valeur: str = "fermeture"):
    params = {
        "début": debut.strftime("%Y-%m-%d"),
        "fin": fin.strftime("%Y-%m-%d")
    }

    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'

    reponse = requests.get(url=url, params=params).json()
    historique = []
    for key, value in reponse["historique"].items():
        historique.append(
            (dt.datetime.strptime(key, "%Y-%m-%d").date(), value[valeur])
        )

    return historique

if __name__ == "__main__":
    fmt = "titre={}: valeur={}, début={}, fin={}"
    args = analyse_de_commande()

    for symbole in args.symbole:
        sym = symbole.lower()
        val = args.valeur
        debut = dt.datetime.strptime(args.debut, '%Y-%m-%d').date()
        fin = dt.datetime.strptime(args.fin, '%Y-%m-%d').date()

        header = fmt.format(sym, val, repr(debut), repr(fin))
        
        print(header)
        print(produire_historique(symbole=sym, debut=debut, fin=fin, valeur=val))