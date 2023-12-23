import datetime
from exceptions import *


class Portefeuille:
    def __init__(self, bourse):
        self.bourse = bourse
        self.liquidites = 10000
        self.actions = {}
        self.transactions = []

    def deposer(self, montant, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        self.liquidites += montant
        self.transactions.append(('deposer', montant, date))

    def solde(self, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        return self.liquidites

    def acheter(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        prix = self.bourse.prix(symbole, date)
        cout = prix * quantite
        if self.liquidites < cout:
            raise LiquiditeInsuffisante()
        self.liquidites -= cout
        self.actions[symbole] = self.actions.get(symbole, 0) + quantite
        self.transactions.append(('acheter', symbole, quantite, date))

    def vendre(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        if self.actions.get(symbole, 0) < quantite:
            raise ErreurQuantite()
        prix = self.bourse.prix(symbole, date)
        revenu = prix * quantite
        self.liquidites += revenu
        self.actions[symbole] -= quantite
        if self.actions[symbole] == 0:
            del self.actions[symbole]
        self.transactions.append(('vendre', symbole, quantite, date))

    def valeur_totale(self, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        total = self.liquidites
        for symbole, quantite in self.actions.items():
            total += self.bourse.prix(symbole, date) * quantite
        return total

    def valeur_des_titres(self, symboles, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        total = 0
        for symbole in symboles:
            total += self.bourse.prix(symbole, date) * self.actions.get(symbole, 0)
        return total

    def titres(self, date=None):
        if date is None:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise ErreurDate()
        return {symbole: quantite for symbole, quantite in self.actions.items()}

    def valeur_projetee(self, date, rendement):
        if date <= datetime.date.today():
            raise ErreurDate()
        valeur = self.valeur_totale(datetime.date.today())
        jours_total = (date - datetime.date.today()).days
        annees_completes = jours_total // 365
        jours_restants = jours_total % 365
        if isinstance(rendement, dict):
            for symbole, qty in self.actions.items():
                taux = rendement.get(symbole, 0) / 100
                valeur += qty * (self.bourse.prix(symbole, datetime.date.today()) *
                                 ((1 + taux) ** annees_completes + (jours_restants / 365) * taux))
        else:
            taux = rendement / 100
            valeur *= (1 + taux) ** annees_completes + (jours_restants / 365) * taux
        return valeur