from argparse import ArgumentParser
from datetime import date
import sys
from portefeuille import Portefeuille 
from bourse import Bourse
from exceptions import ErreurDate, ErreurQuantite, LiquiditeInsuffisante  

def analyser_commande():
    parser = ArgumentParser(description="Gestionnaire de portefeuille d'actions")
    parser.add_argument("action", type=str, choices=['deposer', 'acheter', 'vendre', 'lister', 'projeter'])
    parser.add_argument("-d", "--date", type=lambda s: date.fromisoformat(s), default=date.today())
    parser.add_argument("-q", "--quantite", type=int, default=1)
    parser.add_argument("-t", "--titres", nargs="*", default=[])
    parser.add_argument("-g", "--graphique", action="store_true")
    parser.add_argument("-r", "--rendement", type=float, default=0)
    parser.add_argument("-v", "--volatilite", type=float, default=0)
    parser.add_argument("-p", "--portefeuille", default="folio")
    return parser.parse_args()

def main():
    args = analyser_commande()
    bourse = Bourse()
    portfolio = Portefeuille(bourse, args.portefeuille)  

    try:
        if args.action == 'deposer':
            portfolio.deposer(args.quantite, args.date)
            print(f"solde = {portfolio.solde(args.date):.2f}")

        elif args.action == 'acheter':
            if not args.titres:
                sys.exit("Error: No securities specified for purchase.")
            for symbole in args.titres:
                portfolio.acheter(symbole, args.quantite, args.date)
                print(f"solde = {portfolio.solde(args.date):.2f}")

        elif args.action == 'vendre':
            if not args.titres:
                sys.exit("Error: No securities specified for sale.")
            for symbole in args.titres:
                portfolio.vendre(symbole, args.quantite, args.date)
                print(f"solde = {portfolio.solde(args.date):.2f}")

        elif args.action == 'lister':
            titres = portfolio.titres(args.date)
            for symbole, quantite in titres.items():
                prix = bourse.prix(symbole, args.date)
                montant = quantite * prix
                print(f"{symbole} = {quantite} x {prix:.2f} = {montant:.2f}")

        elif args.action == 'projeter':
            future_date = args.date
            projected_value = portfolio.valeur_projetee(future_date, args.rendement)
            print(f"valeur projetée = {projected_value:.2f}")

    except (ErreurDate, ErreurQuantite, LiquiditeInsuffisante) as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
