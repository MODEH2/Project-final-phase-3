import datetime
from datetime import date
from exceptions import *
import json
import numpy as np


class Portefeuille:
    def __init__(self, bourse, nom_fichier='folio.json'):
        self.bourse = bourse
        self.liquidites = 100000
        self.actions = {}
        self.transactions = []
        self.nom_fichier = nom_fichier
        self.lire_json(nom_fichier)  

    def lire_json(self, nom_fichier):
        try:
            with open(nom_fichier, 'r') as file:
                data = json.load(file)
                self.liquidites = data.get('liquidites', 10000)
                self.actions = data.get('actions', {})
        except FileNotFoundError:
            self.liquidites = 100000
            self.actions = {}
            pass


    def ecrire_json(self, nom_fichier):
        
         data = {
            'liquidites': self.liquidites,
            'actions': self.actions,
            'transactions': [
                {
                    'type': transaction[0],
                    'montant': transaction[1],
                    'date': transaction[2].isoformat() if isinstance(transaction[2], date) else transaction[2]
                } for transaction in self.transactions
            ]
        }
         with open(nom_fichier, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def deposer(self, montant, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate("Future date is not allowed for deposit.")
        self.liquidites += montant
        self.transactions.append(('deposer', montant, date.strftime("%Y-%m-%d")))
        self.ecrire_json(self.nom_fichier)

    def solde(self, date=None):
        if date is None:
            date = datetime.date.today()
        balance = self.liquidites        
        for transaction in self.transactions:
            trans_date = datetime.datetime.strptime(transaction[2], '%Y-%m-%d').date()
            if trans_date <= date:
                if transaction[0] == 'deposer':
                    balance += transaction[1]
                elif transaction[0] == 'acheter':
                    balance -= transaction[1] * self.bourse.prix(transaction[1], trans_date)
                elif transaction[0] == 'vendre':
                    balance += transaction[1] * self.bourse.prix(transaction[1], trans_date)

        return balance
        
    def acheter(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate("Future date is not allowed for buying.")
        cout = self.bourse.prix(symbole, date) * quantite
        if self.liquidites < cout:
            raise LiquiditeInsuffisante("Insufficient funds to buy.")
        self.liquidites -= cout
        self.actions[symbole] = self.actions.get(symbole, 0) + quantite
        self.transactions.append(('acheter', symbole, quantite, date.strftime("%Y-%m-%d")))
        self.ecrire_json(self.nom_fichier)

    def vendre(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate("Future date is not allowed for selling.")
        if symbole not in self.actions or self.actions[symbole] < quantite:
            raise ErreurQuantite("Not enough shares to sell.")
        revenu = self.bourse.prix(symbole, date) * quantite
        self.liquidites += revenu
        self.actions[symbole] -= quantite
        if self.actions[symbole] == 0:
            del self.actions[symbole]
        self.transactions.append(('', symbole, quantite, date.strftime("%Y-%m-%d")))
        self.ecrire_json(self.nom_fichier)

    def valeur_totale(self, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate("Future date is not allowed for total value.")
        total = self.liquidites
        for symbole, quantite in self.actions.items():
            total += self.bourse.prix(symbole, date) * quantite
        return total

    def titres(self, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate("Future date is not allowed for titles.")
        return {symbole: quantite for symbole, quantite in self.actions.items()}

    def valeur_projetee(self, date, rendement, volatilite):
        if date <= datetime.date.today():
            raise ErreurDate("Past date is not allowed for projection.")
        valeur_actuelle = self.valeur_totale()
        jours_total = (date - datetime.date.today()).days
        annees = jours_total // 365
        jours_restants = jours_total % 365
        taux = rendement / 100
        sigma = volatilite / 100
        projections = np.random.normal(taux, sigma, 1000)
        valeur_future = valeur_actuelle * ((1 + projections) ** annees)
        valeur_future += valeur_future * (jours_restants / 365) * projections
        return np.percentile(valeur_future, [25, 50, 75])

    
 