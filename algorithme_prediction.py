# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:40:44 2016

@author: Philippe

Algorithme de prédiction lié aux différents prédicteurs

"""

from numpy import zeros
from datetime import datetime
from constante import ACTIVATION_ANA, ACTIVATION_PARAM, ACTIVATION_REF,\
    ANA_SCENARIO, ANNEE_POINT, DATE_INIT, DEB_MATIN, DEB_MIDI, \
    DEB_SOIR, FILTRE, HEURE_POINT, HORIZON, INTER_POINT, JOUR_POINT, \
    MATIN, MAXI, MIDI, MOIS_POINT, NB_PREDICTEURS, NON_FILTRE,\
    NUIT, PARA_SENS, PRED_RESULTAT, SEQUENCE, SOIR, TAILLE_BUFFER, TIME_HEURE,\
    TYPE_POINT, VAL_ANNEE, VAL_HEURE, VAL_JOUR, VAL_MOIS, VAL_VALEUR, \
    V_PREDIC, V_PREDIC2, V_PREDIC3, PRED_MOYEN, PRED_ECART, REF_SCENARIO, \
    PRED_RANG, PRED_OPTION


def Analyse(valeur, buffer):
    """
    Controle des valeurs d entree :

    sortie :
        res = -1 : donnees non coherente utilisable pour la nouvelle prediction
        res = 0 : donnees actuelle, pas de nouveau calcul a faire
        res = 1 : donnees valable pour un nouveau calcul
    """
    res = 0
    try:
        date_valeur = datetime(int(valeur[VAL_ANNEE]), int(valeur[VAL_MOIS]),
                               int(valeur[VAL_JOUR]), int(valeur[VAL_HEURE]))
    except:
        res = -1
    try:
        date_buffer = datetime(int(buffer[ANNEE_POINT, TAILLE_BUFFER]),
                               int(buffer[MOIS_POINT, TAILLE_BUFFER]),
                               int(buffer[JOUR_POINT, TAILLE_BUFFER]),
                               int(buffer[HEURE_POINT, TAILLE_BUFFER]))
    except:
        res = -1
    if res == 0:
        if date_buffer == date_valeur:
                    res = 0
        elif date_buffer == DATE_INIT or \
                date_valeur - date_buffer == TIME_HEURE:
                    res = 1
        else:
                    res = -1

        # test sommaire a renforcer ensuite ( a partir des minmax identifies)
        if valeur[VAL_VALEUR] < 0. or valeur[VAL_VALEUR] > 1000.:
            res = -1

    return res


def AcquisitionBuffer(valeur, buffer, b_prediction_meilleur):

    # decalage d'un pas de temps des donnees : indice 0 -> la plus ancienne
    for i in range(TAILLE_BUFFER):
        buffer[NON_FILTRE, i] = buffer[NON_FILTRE, i + 1]
        buffer[HEURE_POINT, i] = buffer[HEURE_POINT, i + 1]
        buffer[FILTRE, i] = buffer[FILTRE, i + 1]
        buffer[JOUR_POINT, i] = buffer[JOUR_POINT, i + 1]
        buffer[MOIS_POINT, i] = buffer[MOIS_POINT, i + 1]
        buffer[ANNEE_POINT, i] = buffer[ANNEE_POINT, i + 1]
        buffer[TYPE_POINT, i] = 0
        buffer[SEQUENCE, i] = 0

    # documentation de la derniere donnee (correspond a l'instant t-1)
    buffer[NON_FILTRE, TAILLE_BUFFER] = valeur[VAL_VALEUR]
    buffer[HEURE_POINT, TAILLE_BUFFER] = valeur[VAL_HEURE]
    buffer[JOUR_POINT, TAILLE_BUFFER] = valeur[VAL_JOUR]
    buffer[MOIS_POINT, TAILLE_BUFFER] = valeur[VAL_MOIS]
    buffer[ANNEE_POINT, TAILLE_BUFFER] = valeur[VAL_ANNEE]
    buffer[FILTRE, TAILLE_BUFFER - 1] = 0.5 * \
        buffer[FILTRE, TAILLE_BUFFER - 2] + 0.25 * \
        buffer[NON_FILTRE, TAILLE_BUFFER - 1] + 0.25 * \
        buffer[NON_FILTRE, TAILLE_BUFFER]
    buffer[FILTRE, TAILLE_BUFFER] = 0.5 * \
        buffer[FILTRE, TAILLE_BUFFER - 1] + 0.25 * \
        buffer[NON_FILTRE, TAILLE_BUFFER] + 0.25 * \
        b_prediction_meilleur[0, 1]
    buffer[TYPE_POINT, TAILLE_BUFFER] = 0
    buffer[SEQUENCE, TAILLE_BUFFER] = 0

    # regeneration des donnees calculees
    for i in range(1, TAILLE_BUFFER+1):
        if buffer[HEURE_POINT, i] < DEB_MATIN:
            buffer[SEQUENCE, i] = NUIT
            if buffer[SEQUENCE, i - 1] != NUIT:
                buffer[TYPE_POINT, i] = -1 * PARA_SENS
                mini_seq1 = i
            elif buffer[NON_FILTRE, mini_seq1] * PARA_SENS > \
                    buffer[NON_FILTRE, i] * PARA_SENS:
                buffer[TYPE_POINT, i] = -1 * PARA_SENS
                buffer[TYPE_POINT, mini_seq1] = INTER_POINT
                mini_seq1 = i
        elif buffer[HEURE_POINT, i] < DEB_MIDI:
            buffer[SEQUENCE, i] = MATIN
            if buffer[SEQUENCE, i - 1] != MATIN:
                buffer[TYPE_POINT, i] = 1 * PARA_SENS
                maxi_seq2 = i
            elif buffer[NON_FILTRE, maxi_seq2] * PARA_SENS < \
                    buffer[NON_FILTRE, i] * PARA_SENS:
                buffer[TYPE_POINT, i] = 1 * PARA_SENS
                buffer[TYPE_POINT, maxi_seq2] = INTER_POINT
                maxi_seq2 = i
        elif buffer[HEURE_POINT, i] < DEB_SOIR:
            buffer[SEQUENCE, i] = MIDI
            if buffer[SEQUENCE, i - 1] != MIDI:
                buffer[TYPE_POINT, i] = -1 * PARA_SENS
                mini_seq3 = i
            elif buffer[NON_FILTRE, mini_seq3] * PARA_SENS > \
                    buffer[NON_FILTRE, i] * PARA_SENS:
                buffer[TYPE_POINT, i] = -1 * PARA_SENS
                buffer[TYPE_POINT, mini_seq3] = INTER_POINT
                mini_seq3 = i
        else:
            buffer[SEQUENCE, i] = SOIR
            if buffer[SEQUENCE, i - 1] != SOIR:
                buffer[TYPE_POINT, i] = 1 * PARA_SENS
                maxi_seq4 = i
            elif buffer[NON_FILTRE, maxi_seq4] * PARA_SENS < \
                    buffer[NON_FILTRE, i] * PARA_SENS:
                buffer[TYPE_POINT, i] = 1 * PARA_SENS
                buffer[TYPE_POINT, maxi_seq4] = INTER_POINT
                maxi_seq4 = i


def Mesure_Ecart_Meilleur(ecart_pred_meilleur, b_prediction_meilleur,
                          horizon_pred, buffer):

    # ecart reel / valeurs predites avec horizon de prediction
    # pour chaque type de resultat

    for k in range(HORIZON):
        ecart_pred_meilleur[k] = abs(b_prediction_meilleur[k, k] -
                                     buffer[NON_FILTRE, TAILLE_BUFFER])


def Apprentissage_Prediction(ecart_reference, memoire_moyenne_ana,
                             ecart_pred_analogie, ecart_pred_parametre,
                             coef_predicteur, b_pred_tableau,
                             memoire_prediction):
    tableau = zeros((2, NB_PREDICTEURS))
    rang_pred = zeros((PRED_MOYEN + 1, NB_PREDICTEURS))
    rang_moyen = zeros((NB_PREDICTEURS))

    for k in range(HORIZON):

        # initialisation et tri du tableau des predicteurs
        for i in range(REF_SCENARIO):
            b_pred_tableau[0, PRED_ECART, i, k] = ecart_reference[i, k]
            b_pred_tableau[0, PRED_RANG, i, k] = i
            if not ACTIVATION_REF:
                b_pred_tableau[0, PRED_ECART, i, k] = MAXI
        for i in range(ANA_SCENARIO):
            j = round(memoire_moyenne_ana[i], 0)
            b_pred_tableau[0, PRED_ECART, i + REF_SCENARIO, k] = \
                ecart_pred_analogie[i, j, k]
            b_pred_tableau[0, PRED_RANG, i + REF_SCENARIO, k] = \
                i + REF_SCENARIO
            if not ACTIVATION_ANA:
                b_pred_tableau[0, PRED_ECART, i + REF_SCENARIO, k] = MAXI
        for i in range(PRED_RESULTAT):
            b_pred_tableau[0, PRED_ECART, i+REF_SCENARIO+ANA_SCENARIO, k] = \
                ecart_pred_parametre[i, k]
            b_pred_tableau[0, PRED_RANG, i+REF_SCENARIO+ANA_SCENARIO, k] = \
                i + REF_SCENARIO + ANA_SCENARIO
            if not ACTIVATION_PARAM:
                b_pred_tableau[0, PRED_ECART, i+REF_SCENARIO+ANA_SCENARIO, k] \
                    = MAXI

        # tri tableau (meilleur avec 0, moins bon NB_PREDICTEURS-1)
        taille = NB_PREDICTEURS - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if b_pred_tableau[0, PRED_ECART, i, k] > \
                   b_pred_tableau[0, PRED_ECART, i + 1, k]:
                        interval = b_pred_tableau[0, PRED_ECART, i, k]
                        interrang = b_pred_tableau[0, PRED_RANG, i, k]
                        b_pred_tableau[0, PRED_ECART, i, k] = \
                            b_pred_tableau[0, PRED_ECART, i + 1, k]
                        b_pred_tableau[0, PRED_RANG, i, k] = \
                            b_pred_tableau[0, PRED_RANG, i + 1, k]
                        b_pred_tableau[0, PRED_ECART, i + 1, k] = interval
                        b_pred_tableau[0, PRED_RANG, i + 1, k] = interrang
                        ok = False
            taille = taille - 1

        # pointage invese du tableau (rangpred(n°pred) = rang)
        for h in range(PRED_MOYEN + 1):
            for i in range(NB_PREDICTEURS):
                rang_pred[h, b_pred_tableau[h, PRED_RANG, i, k]] = i

        # lissage des rangs
        for i in range(NB_PREDICTEURS):
            rang_moyen[i] = 0
            for h in range(PRED_MOYEN + 1):
                rang_moyen[i] += rang_pred[h, i]

        # tableau des rang_moyen à trier
        for i in range(NB_PREDICTEURS):
            tableau[0, i] = i
            tableau[1, i] = rang_moyen[i]

        # tri tableau (meilleur: tab(0,0), moins bon: tab(0,NB_PREDICTEURS-1))
        taille = NB_PREDICTEURS - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if tableau[1, i] > tableau[1, i + 1]:
                    interval = tableau[0, i]
                    interrang = tableau[1, i]
                    tableau[0, i] = tableau[0, i + 1]
                    tableau[1, i] = tableau[1, i + 1]
                    tableau[0, i + 1] = interval
                    tableau[1, i + 1] = interrang
                    ok = False
            taille -= 1

        # affectation des nouvelles valeurs des coef des predicteurs
        if PRED_OPTION == 0:
            for i in range(NB_PREDICTEURS):
                coef_predicteur[k, tableau[0, i]] = memoire_prediction[i]
        else:
            coef_predicteur[k, tableau[0, 0]] += V_PREDIC
            coef_predicteur[k, tableau[0, 1]] += V_PREDIC2
            coef_predicteur[k, tableau[0, 2]] += V_PREDIC3
        if PRED_OPTION == 2:
            coef_predicteur[k, tableau[0, NB_PREDICTEURS - 3]] /= 2
            coef_predicteur[k, tableau[0, NB_PREDICTEURS - 2]] /= 4
            coef_predicteur[k, tableau[0, NB_PREDICTEURS - 1]] /= 8

        # remise a 1 de la somme des predicteurs
        total = 0
        for i in range(NB_PREDICTEURS):
            total += coef_predicteur[k, i]
        for i in range(NB_PREDICTEURS):
            coef_predicteur[k, i] /= total


def Decalage_Buffer_Pred_Meilleur(b_pred_filtre, b_prediction_meilleur,
                                  b_pred_tableau):

    for i in range(TAILLE_BUFFER, 0, -1):
        for l in range(HORIZON):
            b_prediction_meilleur[i, l] = b_prediction_meilleur[i - 1, l]
            b_pred_filtre[i, l] = b_pred_filtre[i - 1, l]
            for k in range(NB_PREDICTEURS):
                b_pred_tableau[i, 0, k, l] = b_pred_tableau[i - 1, 0, k, l]
                b_pred_tableau[i, 1, k, l] = b_pred_tableau[i - 1, 1, k, l]


def Meilleure_Prediction(b_pred_filtre, b_prediction_meilleur,
                         b_prediction_reference, b_prediction_analogie,
                         b_prediction_parametre, coef_predicteur,
                         memoire_moyenne_ana, buffer):

    for k in range(HORIZON):
        b_prediction_meilleur[0, k] = 0

        # valeur de reference
        for i in range(REF_SCENARIO):
            b_prediction_meilleur[0, k] += coef_predicteur[k, i] * \
                b_prediction_reference[0, i, k]

        # valeur de predicteur analogie
        for i in range(ANA_SCENARIO):
            j = round(memoire_moyenne_ana[i], 0)
            b_prediction_meilleur[0, k] += \
                coef_predicteur[k, i + REF_SCENARIO] * \
                b_prediction_analogie[0, i, j, k]

        # valeur de predicteur parametre
        for i in range(PRED_RESULTAT):
            b_prediction_meilleur[0, k] += \
                coef_predicteur[k, i + REF_SCENARIO + ANA_SCENARIO] * \
                b_prediction_parametre[0, i, k]

    # calcul des valeurs prévues filtrees
    b_pred_filtre[0, 0] = 0.5 * buffer[FILTRE, TAILLE_BUFFER] + 0.25 * \
        b_prediction_meilleur[0, 0] + 0.25 * b_prediction_meilleur[0, 1]
    for k in range(1, HORIZON - 1):
        b_pred_filtre[0, k] = 0.5 * b_pred_filtre[0, k-1] + 0.25 * \
            b_prediction_meilleur[0, k] + 0.25 * b_prediction_meilleur[0, k+1]
    b_pred_filtre[0, HORIZON - 1] = b_prediction_meilleur[0, HORIZON - 1]
