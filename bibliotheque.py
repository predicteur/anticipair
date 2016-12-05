# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 19:35:33 2016
@author: Philippe
Methode de chargement de la bibliotheque historique
"""

from numpy import loadtxt
from constante import ANNEE_POINT, DEB_MATIN, DEB_MIDI, DEB_SOIR, FILE_BIBLIO,\
    FILTRE, HEURE_POINT, INTER_POINT, JOUR_POINT, MATIN, MAXI, MAX_SEQ, MIDI,\
    MIN_SEQ, MOIS_POINT, NB_SEQ, NON_FILTRE, NUIT, N_LIGNE, PARA_SENS, \
    SEQUENCE, SOIR, TYPE_POINT, V_VENT


def Init_Bibliotheque(serie_a_traiter, serie_vent, donnees, min_max_seq):
    """
    chargement et initialisation de la bibliotheque
    """
    biblio = loadtxt(FILE_BIBLIO, delimiter=';', skiprows=1)

    donnees[NON_FILTRE, 0] = 0.0
    donnees[FILTRE, 0] = 0.0
    donnees[SEQUENCE, 0] = 0
    donnees[TYPE_POINT, 0] = 0
    donnees[HEURE_POINT, 0] = 0
    donnees[JOUR_POINT, 0] = 1
    donnees[MOIS_POINT, 0] = 1
    donnees[ANNEE_POINT, 0] = 1900
    donnees[V_VENT, 0] = 0.0

    donnees[NON_FILTRE, N_LIGNE] = 0
    donnees[FILTRE, N_LIGNE] = 0

    for i in range(1, NB_SEQ+1):
        min_max_seq[i, MIN_SEQ] = MAXI
        min_max_seq[i, MAX_SEQ] = 0.0

    for i in range(1, N_LIGNE):
        donnees[HEURE_POINT, i] = biblio[i - 1, 3]
        donnees[JOUR_POINT, i] = biblio[i - 1, 2]
        donnees[MOIS_POINT, i] = biblio[i - 1, 1]
        donnees[ANNEE_POINT, i] = biblio[i - 1, 0]
        donnees[V_VENT, i] = biblio[i - 1, serie_vent]
        donnees[NON_FILTRE, i] = biblio[i - 1, serie_a_traiter]
        if i > 1:
            donnees[FILTRE, i - 1] = 0.5 * donnees[FILTRE, i - 2] + \
                0.25 * donnees[NON_FILTRE, i - 1] + 0.25 * \
                donnees[NON_FILTRE, i]
        donnees[FILTRE, i] = 0.5 * donnees[FILTRE, i - 1] + 0.25 * \
            donnees[NON_FILTRE, i] + 0.25 * \
            (2 * donnees[NON_FILTRE, i] - donnees[NON_FILTRE, i - 1])

        if donnees[HEURE_POINT, i] < DEB_MATIN:
            donnees[SEQUENCE, i] = NUIT
            if (donnees[NON_FILTRE, i] > 1) and \
               (donnees[NON_FILTRE, i] < min_max_seq[NUIT, MIN_SEQ]):
                min_max_seq[NUIT, MIN_SEQ] = donnees[NON_FILTRE, i]
            elif donnees[NON_FILTRE, i] > min_max_seq[NUIT, MAX_SEQ]:
                min_max_seq[NUIT, MAX_SEQ] = donnees[NON_FILTRE, i]
            if donnees[SEQUENCE, i - 1] != NUIT:
                donnees[TYPE_POINT, i] = -1 * PARA_SENS
                mini_seq1 = i
            elif donnees[NON_FILTRE, mini_seq1] * PARA_SENS >\
                    donnees[NON_FILTRE, i] * PARA_SENS:
                donnees[TYPE_POINT, i] = -1 * PARA_SENS
                donnees[TYPE_POINT, mini_seq1] = INTER_POINT
                mini_seq1 = i
        elif donnees[HEURE_POINT, i] < DEB_MIDI:
            donnees[SEQUENCE, i] = MATIN
            if (donnees[NON_FILTRE, i] > 1) and \
               (donnees[NON_FILTRE, i] < min_max_seq[MATIN, MIN_SEQ]):
                min_max_seq[MATIN, MIN_SEQ] = donnees[NON_FILTRE, i]
            elif donnees[NON_FILTRE, i] > min_max_seq[MATIN, MAX_SEQ]:
                min_max_seq[MATIN, MAX_SEQ] = donnees[NON_FILTRE, i]
            if donnees[SEQUENCE, i - 1] != MATIN:
                donnees[TYPE_POINT, i] = 1 * PARA_SENS
                maxi_seq2 = i
            elif donnees[NON_FILTRE, maxi_seq2] * PARA_SENS < \
                    donnees[NON_FILTRE, i] * PARA_SENS:
                donnees[TYPE_POINT, i] = 1 * PARA_SENS
                donnees[TYPE_POINT, maxi_seq2] = INTER_POINT
                maxi_seq2 = i
        elif donnees[HEURE_POINT, i] < DEB_SOIR:
            donnees[SEQUENCE, i] = MIDI
            if (donnees[NON_FILTRE, i] > 1) and \
               (donnees[NON_FILTRE, i] < min_max_seq[MIDI, MIN_SEQ]):
                min_max_seq[MIDI, MIN_SEQ] = donnees[NON_FILTRE, i]
            elif donnees[NON_FILTRE, i] > min_max_seq[MIDI, MAX_SEQ]:
                min_max_seq[MIDI, MAX_SEQ] = donnees[NON_FILTRE, i]
            if donnees[SEQUENCE, i - 1] != MIDI:
                donnees[TYPE_POINT, i] = -1 * PARA_SENS
                mini_seq3 = i
            elif donnees[NON_FILTRE, mini_seq3] * PARA_SENS > \
                    donnees[NON_FILTRE, i] * PARA_SENS:
                donnees[TYPE_POINT, i] = -1 * PARA_SENS
                donnees[TYPE_POINT, mini_seq3] = INTER_POINT
                mini_seq3 = i
        else:
            donnees[SEQUENCE, i] = SOIR
            if (donnees[NON_FILTRE, i] > 1) and \
               (donnees[NON_FILTRE, i] < min_max_seq[SOIR, MIN_SEQ]):
                min_max_seq[SOIR, MIN_SEQ] = donnees[NON_FILTRE, i]
            elif donnees[NON_FILTRE, i] > min_max_seq[SOIR, MAX_SEQ]:
                min_max_seq[SOIR, MAX_SEQ] = donnees[NON_FILTRE, i]
            if donnees[SEQUENCE, i - 1] != SOIR:
                donnees[TYPE_POINT, i] = 1 * PARA_SENS
                maxi_seq4 = i
            elif donnees[NON_FILTRE, maxi_seq4] * PARA_SENS < \
                    donnees[NON_FILTRE, i] * PARA_SENS:
                donnees[TYPE_POINT, i] = 1 * PARA_SENS
                donnees[TYPE_POINT, maxi_seq4] = INTER_POINT
                maxi_seq4 = i
