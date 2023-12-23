from datetime import date
import datetime as dt
import requests
from exceptions import *


class Bourse:
    def __init__(self):
        pass

    def prix(self, symbole, date_interet):
        if date_interet > dt.date.today():
            raise ErreurDate()
        return self.produire_historique(symbole, date_interet, date_interet)[0][1]

    def produire_historique(self, symbole, debut, fin, valeur="fermeture"):
        params = {
            "debut": debut.strftime("%Y-%m-%d"),
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
    bourse = Bourse()
    args = {
        'symbole': ['AAPL'],
        'debut': '2022-01-01',
        'fin': '2022-01-10',
        'valeur': 'fermeture'
    }
    for symbole in args['symbole']:
        debut = dt.datetime.strptime(args['debut'], '%Y-%m-%d').date()
        fin = dt.datetime.strptime(args['fin'], '%Y-%m-%d').date()
        print(bourse.prix(symbole, fin))
