# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 19:35:33 2016
@author: Philippe
Methode de chargement de la bibliotheque historique
"""

from numpy import loadtxt, percentile

from anticipair.constante import ANNEE_POINT, DEB_MATIN, DEB_MIDI, DEB_SOIR, \
    FILTRE, HEURE_POINT, INTER_POINT, JOUR_POINT, MATIN, MAXI, MAX_SEQ, MIDI,\
    MIN_SEQ, MOIS_POINT, NB_SEQ, NON_FILTRE, NUIT, PARA_SENS, \
    SEQUENCE, SOIR, TYPE_POINT, V_VENT, ECART, ECRETE, SEUIL_ECRETAGE
from anticipair.constante_instal import FILE_BIBLIO, N_LIGNE


def Init_Bibliotheque(serie_a_traiter, serie_vent, data, min_max):
    """
    chargement et initialisation de la bibliotheque
    Structure du fichier csv FILE_BIBLIO :
        annee, mois, jour, heure : colonnes 0 à 3
        mesure : colonne n° serie_a_traiter
        vent : colonne n° serie_vent
    Nombre de ligne traitees : N_LIGNE
    """
    biblio = loadtxt(FILE_BIBLIO, delimiter=';', skiprows=1)

    data[NON_FILTRE, 0] = 0.0
    data[FILTRE, 0] = 0.0
    data[SEQUENCE, 0] = 0
    data[TYPE_POINT, 0] = 0
    data[HEURE_POINT, 0] = 0
    data[JOUR_POINT, 0] = 1
    data[MOIS_POINT, 0] = 1
    data[ANNEE_POINT, 0] = 1900
    data[V_VENT, 0] = 0.0
    data[ECART, 0] = 0.0
    data[ECRETE, 0] = 0.0

    data[NON_FILTRE, N_LIGNE] = 0
    data[FILTRE, N_LIGNE] = 0

    for i in range(1, NB_SEQ+1):
        min_max[i, MIN_SEQ] = MAXI
        min_max[i, MAX_SEQ] = 0.0

    for i in range(1, N_LIGNE):
        data[HEURE_POINT, i] = biblio[i - 1, 3]
        data[JOUR_POINT, i] = biblio[i - 1, 2]
        data[MOIS_POINT, i] = biblio[i - 1, 1]
        data[ANNEE_POINT, i] = biblio[i - 1, 0]
        if serie_vent == -1:
            data[V_VENT, i] = -1.0
        else:
            data[V_VENT, i] = biblio[i - 1, serie_vent]
        data[NON_FILTRE, i] = biblio[i - 1, serie_a_traiter]
        data[ECART, i] = abs(data[NON_FILTRE, i] - data[NON_FILTRE, i-1])
        if i > 1:
            data[FILTRE, i-1] = 0.5 * data[FILTRE, i-2] + 0.25 * \
                data[NON_FILTRE, i-1] + 0.25 * data[NON_FILTRE, i]
        data[FILTRE, i] = 0.5 * data[FILTRE, i-1] + 0.25 * data[NON_FILTRE, i]\
            + 0.25 * (2 * data[NON_FILTRE, i] - data[NON_FILTRE, i-1])

        if data[HEURE_POINT, i] < DEB_MATIN:
            data[SEQUENCE, i] = NUIT
            if (data[NON_FILTRE, i] > 1) and \
               (data[NON_FILTRE, i] < min_max[NUIT, MIN_SEQ]):
                min_max[NUIT, MIN_SEQ] = data[NON_FILTRE, i]
            elif data[NON_FILTRE, i] > min_max[NUIT, MAX_SEQ]:
                min_max[NUIT, MAX_SEQ] = data[NON_FILTRE, i]
            if data[SEQUENCE, i - 1] != NUIT:
                data[TYPE_POINT, i] = -1 * PARA_SENS
                m_seq1 = i
            elif data[NON_FILTRE, m_seq1] * PARA_SENS > \
                    data[NON_FILTRE, i] * PARA_SENS:
                data[TYPE_POINT, i] = -1 * PARA_SENS
                data[TYPE_POINT, m_seq1] = INTER_POINT
                m_seq1 = i

        elif data[HEURE_POINT, i] < DEB_MIDI:
            data[SEQUENCE, i] = MATIN
            if (data[NON_FILTRE, i] > 1) and \
               (data[NON_FILTRE, i] < min_max[MATIN, MIN_SEQ]):
                min_max[MATIN, MIN_SEQ] = data[NON_FILTRE, i]
            elif data[NON_FILTRE, i] > min_max[MATIN, MAX_SEQ]:
                min_max[MATIN, MAX_SEQ] = data[NON_FILTRE, i]
            if data[SEQUENCE, i - 1] != MATIN:
                data[TYPE_POINT, i] = 1 * PARA_SENS
                mx_seq2 = i
            elif data[NON_FILTRE, mx_seq2] * PARA_SENS < \
                    data[NON_FILTRE, i] * PARA_SENS:
                data[TYPE_POINT, i] = 1 * PARA_SENS
                data[TYPE_POINT, mx_seq2] = INTER_POINT
                mx_seq2 = i

        elif data[HEURE_POINT, i] < DEB_SOIR:
            data[SEQUENCE, i] = MIDI
            if (data[NON_FILTRE, i] > 1) and \
               (data[NON_FILTRE, i] < min_max[MIDI, MIN_SEQ]):
                min_max[MIDI, MIN_SEQ] = data[NON_FILTRE, i]
            elif data[NON_FILTRE, i] > min_max[MIDI, MAX_SEQ]:
                min_max[MIDI, MAX_SEQ] = data[NON_FILTRE, i]
            if data[SEQUENCE, i - 1] != MIDI:
                data[TYPE_POINT, i] = -1 * PARA_SENS
                m_seq3 = i
            elif data[NON_FILTRE, m_seq3] * PARA_SENS > \
                    data[NON_FILTRE, i] * PARA_SENS:
                data[TYPE_POINT, i] = -1 * PARA_SENS
                data[TYPE_POINT, m_seq3] = INTER_POINT
                m_seq3 = i
        else:
            data[SEQUENCE, i] = SOIR
            if (data[NON_FILTRE, i] > 1) and \
               (data[NON_FILTRE, i] < min_max[SOIR, MIN_SEQ]):
                min_max[SOIR, MIN_SEQ] = data[NON_FILTRE, i]
            elif data[NON_FILTRE, i] > min_max[SOIR, MAX_SEQ]:
                min_max[SOIR, MAX_SEQ] = data[NON_FILTRE, i]
            if data[SEQUENCE, i - 1] != SOIR:
                data[TYPE_POINT, i] = 1 * PARA_SENS
                mx_seq4 = i
            elif data[NON_FILTRE, mx_seq4] * PARA_SENS < \
                    data[NON_FILTRE, i] * PARA_SENS:
                data[TYPE_POINT, i] = 1 * PARA_SENS
                data[TYPE_POINT, mx_seq4] = INTER_POINT
                mx_seq4 = i
    seuil = percentile(data[ECART, :], SEUIL_ECRETAGE)

    for i in range(1, N_LIGNE):
        if data[NON_FILTRE, i] - data[ECRETE, i-1] > seuil:
            data[ECRETE, i] = data[ECRETE, i-1] + seuil
        else:
            data[ECRETE, i] = data[NON_FILTRE, i]
    return seuil
