# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:45:55 2016

@author: Philippe

Procédures du prédicteur de référence
"""

from constante import HORIZON, REF_SCENARIO, NON_FILTRE, TAILLE_BUFFER, \
    REF_PENTE, HEURE_POINT, DEB_MATIN, MATIN, DEB_MIDI, MIDI, DEB_SOIR, SOIR, \
    NUIT, MIN_SEQ, MAX_SEQ


def Mesure_Ecart_Reference(ecart_reference, b_prediction_reference, buffer):

    for k in range(HORIZON):
        for j in range(REF_SCENARIO):
            ecart_reference[j, k] = abs(b_prediction_reference[k, j, k] -
                                        buffer[NON_FILTRE, TAILLE_BUFFER])


def Decalage_Buffer_Pred_Reference(b_prediction_reference):

    for i in range(TAILLE_BUFFER, 0, -1):
        for k in range(REF_SCENARIO):
            for l in range(HORIZON):
                b_prediction_reference[i, k, l] = \
                    b_prediction_reference[i - 1, k, l]


def Predicteur_Reference(b_prediction_reference, b_prediction_meilleur,
                         b_pred_filtre, buffer, min_max_seq):

    valeur_pred_ref = buffer[NON_FILTRE, TAILLE_BUFFER] + REF_PENTE * \
        (buffer[NON_FILTRE, TAILLE_BUFFER] -
         buffer[NON_FILTRE, TAILLE_BUFFER - 1])

    for k in range(HORIZON):
        b_prediction_reference[0, 0, k] = \
            min_max(valeur_pred_ref, buffer[HEURE_POINT, TAILLE_BUFFER] + 1,
                    min_max_seq)
        if k == HORIZON - 1:
            b_prediction_reference[0, 1, k] = b_prediction_meilleur[1, k]
            b_prediction_reference[0, 2, k] = b_pred_filtre[1, k]
        else:
            b_prediction_reference[0, 1, k] = b_prediction_meilleur[1, k + 1]
            b_prediction_reference[0, 2, k] = b_pred_filtre[1, k + 1]


def min_max(valeur, heure, min_max_seq):
    """
     limitation aux valeurs identifiées
    """

    heure = heure % 24

    if heure < DEB_MATIN:
        seq = MATIN
    elif heure < DEB_MIDI:
        seq = MIDI
    elif heure < DEB_SOIR:
        seq = SOIR
    else:
        seq = NUIT

    if valeur < min_max_seq[seq, MIN_SEQ]:
        valeur = min_max_seq[seq, MIN_SEQ]
    elif valeur > min_max_seq[seq, MAX_SEQ]:
        valeur = min_max_seq[seq, MAX_SEQ]

    return valeur
