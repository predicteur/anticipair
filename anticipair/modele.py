# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:32:14 2016

@author: Philippe

Procédures du prédicteur lié a la modelisation

"""

from anticipair.constante import HORIZON, NON_FILTRE, BUF_SERIE, V_MODELE, \
    T_BUFFER, MODELE_SCENARIO, MODELE_PRED, MODELE_MIN, HEURE_POINT
from anticipair.reference import min_max


def Predicteur_Correlation_Modele(b_pred_mod, b_pred_meil, modele,
                                  buffer, min_max_seq):
    """
    calcul de la prediction modele par correlation avec les previsions
    """
    for k in range(HORIZON):
        valeur_modele = 0.0
        valeur_mesure = 0.0
        if MODELE_PRED:
            if k - 1 >= 0:
                for i in range(k):
                    valeur_mesure += b_pred_meil[0, k - i]
                    valeur_modele += 1 / max(modele[k - i], MODELE_MIN)
                    b_pred_mod[0, i, k] = valeur_mesure / valeur_modele / \
                        max(modele[k + 1], MODELE_MIN)

            if MODELE_SCENARIO - 1 >= k:
                for i in range(k, MODELE_SCENARIO):
                    valeur_mesure += buffer[BUF_SERIE, T_BUFFER + k - i]
                    valeur_modele += 1 / max(buffer[V_MODELE, T_BUFFER+k-i],
                                             MODELE_MIN)
                    b_pred_mod[0, i, k] = valeur_mesure / valeur_modele / \
                        max(modele[k + 1], MODELE_MIN)
        else:
            for i in range(MODELE_SCENARIO):
                valeur_mesure += buffer[BUF_SERIE, T_BUFFER - i]
                valeur_modele += 1 / max(buffer[V_MODELE, T_BUFFER-i],
                                         MODELE_MIN)
                b_pred_mod[0, i, k] = valeur_mesure / valeur_modele / \
                    max(modele[k + 1], MODELE_MIN)

    # limitation des valeurs predites
    for i in range(MODELE_SCENARIO):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_mod[0, i, k] = \
                min_max(b_pred_mod[0, i, k], valeur_avant,
                        buffer[HEURE_POINT, T_BUFFER] + 1, min_max_seq)
            valeur_avant = b_pred_mod[0, i, k]

    return b_pred_mod[0, :, :]
