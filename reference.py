# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:45:55 2016

@author: Philippe

Procédures du prédicteur de référence
"""

from constante import HORIZON, REF_SCENARIO, NON_FILTRE, TAILLE_BUFFER, \
    REF_PENTE, HEURE_POINT, DEB_MATIN, MATIN, DEB_MIDI, MIDI, DEB_SOIR, SOIR, \
    NUIT, MIN_SEQ, MAX_SEQ


def Decalage_Buffer_Pred_Reference(b_pred_reference):
    """
    decalage d'un pas de temps
    """
    for i in range(TAILLE_BUFFER, 0, -1):
        for k in range(REF_SCENARIO):
            for l in range(HORIZON):
                b_pred_reference[i, k, l] = b_pred_reference[i - 1, k, l]


def Predicteur_Reference(b_pred_reference, b_pred_meilleur,
                         b_pred_filtre, buffer, min_max_seq):
    """
    calcul des valeurs des predicteurs de reference
    """
    valeur_pred_ref = buffer[NON_FILTRE, TAILLE_BUFFER] + REF_PENTE * \
        (buffer[NON_FILTRE, TAILLE_BUFFER] -
         buffer[NON_FILTRE, TAILLE_BUFFER - 1])
    valeur_pred_ref1 = 0.0
    for i in range(1, TAILLE_BUFFER+1):
        valeur_pred_ref1 += buffer[NON_FILTRE, i] / TAILLE_BUFFER

    for k in range(HORIZON):
        b_pred_reference[0, 0, k] = \
            min_max(valeur_pred_ref, buffer[HEURE_POINT, TAILLE_BUFFER] + 1,
                    min_max_seq)
        b_pred_reference[0, 3, k] = valeur_pred_ref1
        if k == HORIZON - 1:
            b_pred_reference[0, 1, k] = b_pred_meilleur[1, k]
            b_pred_reference[0, 2, k] = b_pred_filtre[1, k]
        else:
            b_pred_reference[0, 1, k] = b_pred_meilleur[1, k + 1]
            b_pred_reference[0, 2, k] = b_pred_filtre[1, k + 1]


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
