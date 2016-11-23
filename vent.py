# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:32:14 2016

@author: Philippe

Procédures du prédicteur vent

"""


from constante import HORIZON, NON_FILTRE, V_VENT, \
    TAILLE_BUFFER, VENT_SCENARIO, VENT_PRED, PARA_SENS, VENT_MIN


def Decalage_Buffer_Pred_Vent(b_pred_vent):
    """
    decalage d'un pas de temps
    """
    for i in range(TAILLE_BUFFER, 0, -1):
        for k in range(VENT_SCENARIO):
            for l in range(HORIZON):
                b_pred_vent[i, k, l] = b_pred_vent[i - 1, k, l]


def Predicteur_Correlation_Vent(b_pred_vent, b_pred_meilleur, vitesse_vent,
                                buffer):
    """
    calcul de la prediction vent
    """
    for k in range(HORIZON):
        valeur_vent = 0.0
        valeur_mesure = 0.0
        if VENT_PRED:
            if k - 1 >= 0:
                for i in range(k):
                    valeur_mesure += b_pred_meilleur[0, k - i]
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
                    valeur_mesure += buffer[NON_FILTRE, TAILLE_BUFFER + k - i]
                    if PARA_SENS == 1:
                        valeur_vent += 1 / max(buffer[V_VENT, TAILLE_BUFFER +
                                                      k - i], VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent / \
                            max(vitesse_vent[k + 1], VENT_MIN)
                    else:
                        valeur_vent += max(buffer[V_VENT, TAILLE_BUFFER +
                                                  k - i], VENT_MIN)
                        b_pred_vent[0, i, k] = valeur_mesure / valeur_vent * \
                            max(vitesse_vent[k + 1], VENT_MIN)
        else:
            for i in range(VENT_SCENARIO):
                valeur_mesure += buffer[NON_FILTRE, TAILLE_BUFFER - i]
                if PARA_SENS == 1:
                    valeur_vent += 1 / max(buffer[V_VENT, TAILLE_BUFFER - i],
                                           VENT_MIN)
                    b_pred_vent[0, i, k] = valeur_mesure / valeur_vent / \
                        max(vitesse_vent[k + 1], VENT_MIN)
                else:
                    valeur_vent += max(buffer[V_VENT, TAILLE_BUFFER - i],
                                       VENT_MIN)
                    b_pred_vent[0, i, k] = valeur_mesure / valeur_vent * \
                        max(vitesse_vent[k + 1], VENT_MIN)
