#!/usr/bin/env python3.5
# coding: utf-8

"""Test Anticipair."""

import os
import datetime
import unittest

import pandas

import anticipair.predicteur as predicteur
from anticipair import constante_instal


class TestAnticipair(unittest.TestCase):
    def test_predicteur(self):
        mesure = 'N2CINQ'

        # Lecture du jeu de données test
        fndat = os.path.join('data', 'data.csv')
        dat = pandas.read_csv(fndat, sep=',', parse_dates=[0, ],
                              index_col=('dateheure',))

        # Préparation des données
        dat['annee'] = dat.index.year
        dat['mois'] = dat.index.month
        dat['jour'] = dat.index.day
        dat['heure'] = dat.index.hour
        dat = dat.dropna()

        # Anticipair
        resultat = None
        pred = predicteur.predicteur(constante_instal.__dict__[mesure],
                                     reset_prediction=True)
        for i, enr in dat.iterrows():
            resultat = pred.Prediction(
                [enr[mesure], enr['heure'], enr['jour'], enr['mois'],
                 enr['annee']])

        # Vérification
        self.assertEqual(
            pred.Info_Date(), datetime.datetime(2017, 1, 17, 14, 0, 0))
        self.assertEqual(len(resultat), 6)
        self.assertEqual(round(resultat[0]), 32)
        self.assertEqual(round(resultat[1]), 38)
        self.assertEqual(round(resultat[2]), 48)
        self.assertEqual(round(resultat[3]), 54)
        self.assertEqual(round(resultat[4]), 53)
        self.assertEqual(round(resultat[5]), 47)


if __name__ == '__main__':
    unittest.main()
