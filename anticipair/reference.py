# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:45:55 2016

@author: Philippe

Procédures du prédicteur de référence
"""

from anticipair.constante import HORIZON, NON_FILTRE, T_BUFFER, BUF_SERIE, \
    REF_PENTE, HEURE_POINT, DEB_MATIN, MATIN, DEB_MIDI, MIDI, DEB_SOIR, SOIR, \
    NUIT, MAX_SEQ, MAX_VARIATION, REF_SCENARIO, MAX_VALEUR, REF_MOYENNE


def Predicteur_Reference(b_pred_ref, b_pred_meil, b_pred_filt, buffer,
                         min_max_seq):
    """
    calcul des valeurs des predicteurs de reference
    """
    # calcul des valeurs predites
    valeur_pred_ref = buffer[BUF_SERIE, T_BUFFER] + REF_PENTE * \
        (buffer[BUF_SERIE, T_BUFFER] - buffer[BUF_SERIE, T_BUFFER - 1])
    valeur_pred_ref1 = 0.0
    for i in range(T_BUFFER-REF_MOYENNE+1, T_BUFFER+1):
        valeur_pred_ref1 += buffer[BUF_SERIE, i] / REF_MOYENNE

    # affectation des valeurs predites
    for k in range(HORIZON):
        b_pred_ref[0, 0, k] = valeur_pred_ref
        b_pred_ref[0, 3, k] = valeur_pred_ref1
        if k == HORIZON - 1:
            b_pred_ref[0, 1, k] = b_pred_meil[1, k]
            b_pred_ref[0, 2, k] = b_pred_filt[1, k]
        else:
            b_pred_ref[0, 1, k] = b_pred_meil[1, k + 1]
            b_pred_ref[0, 2, k] = b_pred_filt[1, k + 1]

    # limitation des valeurs predites
    for i in range(REF_SCENARIO):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_ref[0, i, k] = \
                min_max(b_pred_ref[0, i, k], valeur_avant,
                        buffer[HEURE_POINT, T_BUFFER] + 1, min_max_seq)
            valeur_avant = b_pred_ref[0, i, k]

    return b_pred_ref[0, :, :]


def min_max(valeur, valeur_avant, heure, min_max_seq):
    """
     limitation aux valeurs identifiées
    """
    # valeurinit = valeur
    valeur = max(0.0, valeur)

    heure = heure % 24
    if heure < DEB_MATIN:
        seq = MATIN
    elif heure < DEB_MIDI:
        seq = MIDI
    elif heure < DEB_SOIR:
        seq = SOIR
    else:
        seq = NUIT

    if valeur > MAX_VALEUR * min_max_seq[seq, MAX_SEQ]:
        valeur = MAX_VALEUR * min_max_seq[seq, MAX_SEQ]
        # print('seq + valeur + init max', seq, valeur, valeurinit)

    if valeur - valeur_avant > MAX_VARIATION * min_max_seq[seq, MAX_SEQ]:
        valeur = valeur_avant + MAX_VARIATION * min_max_seq[seq, MAX_SEQ]
        # print('valeur + init varMAX', valeur, valeurinit)
    elif valeur - valeur_avant < -MAX_VARIATION * min_max_seq[seq, MAX_SEQ]:
        valeur = valeur_avant - MAX_VARIATION * min_max_seq[seq, MAX_SEQ]
        # print('valeur + init varMIN', valeur, valeurinit)
    return valeur
