from argparse import ArgumentParser
from datetime import date
import sys
from portefeuille import Portefeuille
from bourse import Bourse
from exceptions import ErreurDate, ErreurQuantite, LiquiditeInsuffisante

def analyser_commande():
    parser = ArgumentParser(description="Gestionnaire de portefeuille d'actions")

    parser.add_argument("-d", "--date",
                        type=lambda s: date.fromisoformat(s),
                        default=date.today(),
                        help="Date effective (par défaut, date du jour)")
    parser.add_argument("-q", "--quantite",
                        type=int,
                        default=1,
                        help="Quantité désirée (par défaut: 1)")
    parser.add_argument("-t", "--titres",
                        type=str,
                        nargs="+",
                        default=None,
                        help="Titres à considérer (séparés par des espaces, p.ex. goog appl msft)")
    parser.add_argument("-g", "--graphique",
                        action="store_true",
                        help="Affichage graphique (par défaut, pas d'affichage graphique)")
    parser.add_argument("-r", "--rendement",
                        type=float,
                        default=0,
                        help="Rendement annuel global (par défaut, 0)")
    parser.add_argument("-v", "--volatilite",
                        type=float,
                        default=0,
                        help="Indice de volatilité global sur le rendement annuel (par défaut, 0)")
    parser.add_argument("-p", "--portefeuille",
                        type=str,
                        default="folio",
                        help="Nom de portefeuille (par défaut, utiliser folio)")

    args = parser.parse_args()
    return args

def main():
    args = analyser_commande()
    bourse = Bourse()
    portfolio = Portefeuille(bourse)

    if args.titres:
        for titre in args.titres:
            try:
                print(f"Prix du titre {titre} à la date {args.date}: {bourse.prix(titre, args.date)}")
            except ErreurDate as e:
                print(f"Erreur: {e}")
    
        pass


if __name__ == "__main__":
    main()
