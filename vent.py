# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:32:14 2016

@author: Philippe

Procédures du prédicteur vent

"""


from constante import HORIZON, NON_FILTRE, V_VENT, T_BUFFER, VENT_SCENARIO, \
    VENT_PRED, PARA_SENS, VENT_MIN, HEURE_POINT, BUF_SERIE
from reference import min_max


def Predicteur_Correlation_Vent(b_pred_vent, b_pred_meil, vitesse_vent,
                                buffer, min_max_seq):
    """
    calcul de la prediction vent
    """
    for k in range(HORIZON):
        valeur_vent = 0.0
        valeur_mesure = 0.0
        if VENT_PRED:
            if k - 1 >= 0:
                for i in range(k):
                    valeur_mesure += b_pred_meil[0, k - i]
                    if PARA_SENS == 1:
                        valeur_vent += 1 / max(vitesse_vent[k - i], VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent / \
                            max(vitesse_vent[k + 1], VENT_MIN)
                    else:
                        valeur_vent += max(vitesse_vent[k - i], VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent * \
                            max(vitesse_vent[k + 1], VENT_MIN)

            if VENT_SCENARIO - 1 >= k:
                for i in range(k, VENT_SCENARIO):
                    valeur_mesure += buffer[BUF_SERIE, T_BUFFER + k - i]
                    if PARA_SENS == 1:
                        valeur_vent += 1 / max(buffer[V_VENT, T_BUFFER+k-i],
                                               VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent / \
                            max(vitesse_vent[k + 1], VENT_MIN)
                    else:
                        valeur_vent += max(buffer[V_VENT, T_BUFFER+k-i],
                                           VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent * \
                            max(vitesse_vent[k + 1], VENT_MIN)
        else:
            for i in range(VENT_SCENARIO):
                valeur_mesure += buffer[BUF_SERIE, T_BUFFER - i]
                if PARA_SENS == 1:
                    valeur_vent += 1 / max(buffer[V_VENT, T_BUFFER-i],
                                           VENT_MIN)
                    b_pred_vent[0, i, k] = valeur_mesure / valeur_vent / \
                        max(vitesse_vent[k + 1], VENT_MIN)
                else:
                    valeur_vent += max(buffer[V_VENT, T_BUFFER - i], VENT_MIN)
                    b_pred_vent[0, i, k] = valeur_mesure / valeur_vent * \
                        max(vitesse_vent[k + 1], VENT_MIN)

    # limitation des valeurs predites
    for i in range(VENT_SCENARIO):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_vent[0, i, k] = \
                min_max(b_pred_vent[0, i, k], valeur_avant,
                        buffer[HEURE_POINT, T_BUFFER] + 1, min_max_seq)
            valeur_avant = b_pred_vent[0, i, k]

    return b_pred_vent[0, :, :]
