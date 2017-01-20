# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:40:44 2016

@author: Philippe

Algorithme de prédiction lié aux différents prédicteurs
Methodes communes
"""

from numpy import zeros, argsort, ones
from datetime import datetime
from reference import min_max
from constante import ACTIVATION_ANA, ACTIVATION_PARAM, ACTIVATION_REF,\
    ANA_SCENARIO, ANNEE_POINT, DATE_INIT, DEB_MATIN, DEB_MIDI, \
    DEB_SOIR, FILTRE, HEURE_POINT, HORIZON, INTER_POINT, JOUR_POINT, \
    MATIN, MIDI, MOIS_POINT, NB_PREDICTEURS, NON_FILTRE,\
    NUIT, PARA_SENS, PRED_RESULTAT, SEQUENCE, SOIR, T_BUFFER, TIME_HEURE,\
    TYPE_POINT, VAL_ANNEE, VAL_HEURE, VAL_JOUR, VAL_MOIS, VAL_VALEUR, \
    V_PREDIC, V_PREDIC2, V_PREDIC3, PRED_ECART, REF_SCENARIO, \
    PRED_RANG, V_VENT, I_REF, I_ANA, I_PARAM, I_VENT, I_ALGO, I_MODELE, \
    VENT_SCENARIO, NB_ALGO, I_MEILLEUR, V_PRED_MOYEN, N_ECART, N_PREDIC, \
    N_PREDIC2, N_PREDIC3, N_MEMOIRE, N_PENAL, OPTI_ALGO, \
    ACTIVATION_VENT, V_MODELE, MODELE_SCENARIO, ACTIVATION_MODELE, \
    NB_PRED_REDUIT, MAXI, NB_ALGO_REDUIT, ECART, ECRETE


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
        date_buffer = datetime(int(buffer[ANNEE_POINT, T_BUFFER]),
                               int(buffer[MOIS_POINT, T_BUFFER]),
                               int(buffer[JOUR_POINT, T_BUFFER]),
                               int(buffer[HEURE_POINT, T_BUFFER]))
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
        if valeur[VAL_VALEUR] < 0. or valeur[VAL_VALEUR] > 1000.0:
            res = -1

    return res


def AcquisitionBuffer(valeur, vitesse_vent, modele, buffer, b_pred_meil,
                      seuil):
    """
    Acquisition du buffer a partir de valeur, vitesse_vent et modele
    """
    # decalage d'un pas de temps des donnees : indice 0 -> la plus ancienne
    for i in range(T_BUFFER):
        buffer[NON_FILTRE, i] = buffer[NON_FILTRE, i + 1]
        buffer[HEURE_POINT, i] = buffer[HEURE_POINT, i + 1]
        buffer[FILTRE, i] = buffer[FILTRE, i + 1]
        buffer[JOUR_POINT, i] = buffer[JOUR_POINT, i + 1]
        buffer[MOIS_POINT, i] = buffer[MOIS_POINT, i + 1]
        buffer[ANNEE_POINT, i] = buffer[ANNEE_POINT, i + 1]
        buffer[V_VENT, i] = buffer[V_VENT, i + 1]
        buffer[V_MODELE, i] = buffer[V_MODELE, i + 1]
        buffer[TYPE_POINT, i] = 0
        buffer[SEQUENCE, i] = 0
        buffer[ECART, i] = buffer[ECART, i + 1]
        buffer[ECRETE, i] = buffer[ECRETE, i + 1]

    # documentation de la derniere donnee (correspond a l'instant t-1)
    buffer[V_MODELE, T_BUFFER] = modele[0]
    buffer[V_VENT, T_BUFFER] = vitesse_vent[0]
    buffer[NON_FILTRE, T_BUFFER] = valeur[VAL_VALEUR]
    buffer[HEURE_POINT, T_BUFFER] = valeur[VAL_HEURE]
    buffer[JOUR_POINT, T_BUFFER] = valeur[VAL_JOUR]
    buffer[MOIS_POINT, T_BUFFER] = valeur[VAL_MOIS]
    buffer[ANNEE_POINT, T_BUFFER] = valeur[VAL_ANNEE]
    buffer[FILTRE, T_BUFFER-1] = 0.5 * buffer[FILTRE, T_BUFFER-2] + 0.25 * \
        buffer[NON_FILTRE, T_BUFFER-1] + 0.25 * buffer[NON_FILTRE, T_BUFFER]
    buffer[FILTRE, T_BUFFER] = 0.5 * buffer[FILTRE, T_BUFFER-1] + 0.25 * \
        buffer[NON_FILTRE, T_BUFFER] + 0.25 * b_pred_meil[0, 1]
    buffer[TYPE_POINT, T_BUFFER] = 0
    buffer[SEQUENCE, T_BUFFER] = 0
    buffer[ECART, T_BUFFER] = abs(buffer[NON_FILTRE, T_BUFFER] -
                                  buffer[NON_FILTRE, T_BUFFER-1])
    if buffer[NON_FILTRE, T_BUFFER] - buffer[ECRETE, T_BUFFER-1] > seuil:
        buffer[ECRETE, T_BUFFER] = buffer[ECRETE, T_BUFFER-1] + seuil
    else:
        buffer[ECRETE, T_BUFFER] = buffer[NON_FILTRE, T_BUFFER]

    # regeneration des donnees calculees
    for i in range(1, T_BUFFER+1):
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


def Mesure_Ecart_Predicteur(ecart_pred, b_pred_algo, b_pred_unit, b_pred_meil,
                            b_pred_filt, buffer):
    """
    Calcul de l'écart entre prediction et valeur mesurée
    """
    # ecart reel / valeurs predites avec horizon de prediction
    for k in range(HORIZON):
        for j in range(I_REF, I_ALGO):
            ecart_pred[j, k] = abs(b_pred_unit[k, j-I_REF, k] -
                                   buffer[NON_FILTRE, T_BUFFER])
        for j in range(I_ALGO, I_MEILLEUR):
            ecart_pred[j, k] = abs(b_pred_algo[k, j-I_ALGO, k] -
                                   buffer[NON_FILTRE, T_BUFFER])
        ecart_pred[I_MEILLEUR, k] = abs(b_pred_meil[k, k] -
                                        buffer[NON_FILTRE, T_BUFFER])
        ecart_pred[I_MEILLEUR+1, k] = abs(b_pred_filt[k, k] -
                                          buffer[NON_FILTRE, T_BUFFER])


def Apprentissage_Prediction(ecart_pred, coef_pred, b_pred_tab, mem_pred,
                             algo_param, desactiv_vent, desactiv_modele,
                             b_pred_unit, buffer):
    """
    calcul des coeff des predicteurs algo a partir des predicteurs élémentaires
    """
    rang_pred = zeros((V_PRED_MOYEN + 1, NB_PREDICTEURS), dtype=int)
    rang_moyen = zeros((NB_PREDICTEURS), dtype=int)
    vitesse = zeros((HORIZON, NB_PREDICTEURS))
    pr = zeros((HORIZON, NB_PRED_REDUIT), dtype=int)
    pr0 = zeros((HORIZON, NB_PREDICTEURS - NB_PRED_REDUIT), dtype=int)

    for k in range(HORIZON):

        # calcul erreur cumulee
        ecart = zeros(NB_PREDICTEURS)
        for i in range(NB_PREDICTEURS):
            for j in range(T_BUFFER-k):
                ecart[i] += abs(b_pred_unit[k+j, i, k] - buffer[NON_FILTRE,
                                                                T_BUFFER - j])
            ecart[i] /= T_BUFFER - k - 1
        rang = argsort(ecart)

        # predicteurs conservés
        for i in range(NB_PRED_REDUIT):
            pr[k, i] = rang[i]

        # predicteurs supprimés (essai)
        for i in range(NB_PREDICTEURS - NB_PRED_REDUIT):
            pr0[k, i] = rang[i + NB_PRED_REDUIT]

        # initialisation du tableau
        for i in range(NB_PRED_REDUIT):
            b_pred_tab[0, PRED_ECART, pr[k, i], k] = ecart_pred[pr[k, i], k]
            b_pred_tab[0, PRED_RANG, pr[k, i], k] = pr[k, i]
        for i in range(NB_PREDICTEURS - NB_PRED_REDUIT):
            b_pred_tab[0, PRED_ECART, pr0[k, i], k] = MAXI
            b_pred_tab[0, PRED_RANG, pr0[k, i], k] = pr0[k, i]

        # tri tableau (meilleur avec i=0, moins bon i=NB_PREDICTEURS-1)
        taille = NB_PREDICTEURS - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if b_pred_tab[0, PRED_ECART, i, k] > \
                   b_pred_tab[0, PRED_ECART, i + 1, k]:
                    interval = b_pred_tab[0, PRED_ECART, i, k]
                    interrang = b_pred_tab[0, PRED_RANG, i, k]
                    b_pred_tab[0, PRED_ECART, i, k] = \
                        b_pred_tab[0, PRED_ECART, i + 1, k]
                    b_pred_tab[0, PRED_RANG, i, k] = \
                        b_pred_tab[0, PRED_RANG, i + 1, k]
                    b_pred_tab[0, PRED_ECART, i + 1, k] = interval
                    b_pred_tab[0, PRED_RANG, i + 1, k] = interrang
                    ok = False
            taille = taille - 1

        # pointage invese du tableau (rangpred(n°pred) = rang)
        for h in range(V_PRED_MOYEN + 1):
            for i in range(NB_PREDICTEURS):
                rang_pred[h, int(b_pred_tab[h, PRED_RANG, i, k])] = i

        # lissage des rangs
        for i in range(NB_PREDICTEURS):
            rang_moyen[i] = 0
            for h in range(V_PRED_MOYEN + 1):
                rang_moyen[i] += rang_pred[h, i]

        # tableau des rang_moyen trié
        rang = argsort(rang_moyen)

        # affectation des nouvelles valeurs des coef des predicteurs
        for j in range(NB_ALGO):
            if algo_param[j, N_ECART] > 0:
                total = 0.0
                for i in range(NB_PRED_REDUIT):
                    vitesse[k, rang[i]] = 1 / max(b_pred_tab[0, PRED_ECART,
                                                  rang[i], k], 0.01)
                    total += vitesse[k, rang[i]]
                for i in range(NB_PRED_REDUIT):
                    coef_pred[k, int(b_pred_tab[0, PRED_RANG, rang[i], k]), j] \
                        += algo_param[j, N_ECART] * vitesse[k, rang[i]] / total
            elif algo_param[j, N_MEMOIRE] > 0:
                for i in range(NB_PRED_REDUIT):
                    coef_pred[k, rang[i], j] = algo_param[j, N_MEMOIRE] * \
                        coef_pred[k, rang[i], j] + mem_pred[i]
            else:
                coef_pred[k, rang[0], j] += algo_param[j, N_PREDIC]
                coef_pred[k, rang[1], j] += algo_param[j, N_PREDIC2]
                coef_pred[k, rang[2], j] += algo_param[j, N_PREDIC3]
            if algo_param[j, N_PENAL] > 0:
                coef_pred[k, rang[NB_PRED_REDUIT - 3], j] = \
                    max(0, coef_pred[k, rang[NB_PRED_REDUIT-3], j] - V_PREDIC3)
                coef_pred[k, rang[NB_PRED_REDUIT - 2], j] = \
                    max(0, coef_pred[k, rang[NB_PRED_REDUIT-2], j] - V_PREDIC2)
                coef_pred[k, rang[NB_PRED_REDUIT - 1], j] = \
                    max(0, coef_pred[k, rang[NB_PRED_REDUIT-1], j] - V_PREDIC)

            # predicteurs supprimés
            for i in range(NB_PREDICTEURS - NB_PRED_REDUIT):
                coef_pred[k, pr0[k, i], j] = 0.0

            # forcage a 0 des coef des predicteurs desactives
            if not ACTIVATION_REF:
                for i in range(REF_SCENARIO):
                    coef_pred[k, i + I_REF, j] = 0.0
            if not ACTIVATION_ANA:
                for i in range(ANA_SCENARIO):
                    coef_pred[k, i + I_ANA, j] = 0.0
            if not ACTIVATION_PARAM:
                for i in range(PRED_RESULTAT):
                    coef_pred[k, i + I_PARAM, j] = 0.0
            if desactiv_vent or not ACTIVATION_VENT:
                for i in range(VENT_SCENARIO):
                    coef_pred[k, i + I_VENT, j] = 0.0
            if desactiv_modele or not ACTIVATION_MODELE:
                for i in range(MODELE_SCENARIO):
                    coef_pred[k, i + I_MODELE, j] = 0.0

            # remise a 1 de la somme des predicteurs
            total = 0.0
            for i in range(NB_PREDICTEURS):
                total += coef_pred[k, i, j]
            for i in range(NB_PREDICTEURS):
                coef_pred[k, i, j] /= total


def Meilleure_Prediction(b_pred_algo, b_pred_filt, b_pred_unit,
                         b_pred_meil, coef_algo, coef_pred, buffer,
                         min_max_seq):
    """
    calcul des prediction algo a partir des predicteurs elementaires
    """
    # calcul des valeurs prévues par algorithme
    for l in range(NB_ALGO):
        for k in range(HORIZON):
            b_pred_algo[0, l, k] = 0.0
            for i in range(NB_PREDICTEURS):
                b_pred_algo[0, l, k] += coef_pred[k, i, l] * b_pred_unit[0, i,
                                                                         k]

    # limitation des valeurs predites
    for i in range(NB_ALGO):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_algo[0, i, k] = min_max(b_pred_algo[0, i, k], valeur_avant,
                                           buffer[HEURE_POINT, T_BUFFER] + 1,
                                           min_max_seq)
            valeur_avant = b_pred_algo[0, i, k]

    # calcul des meilleures valeurs prevues
    for k in range(HORIZON):
        b_pred_meil[0, k] = 0.0
        for i in range(NB_ALGO):
            b_pred_meil[0, k] += (coef_algo[k, i] * b_pred_algo[0, i, k])

    # limitation des valeurs predites
    valeur_avant = buffer[NON_FILTRE, T_BUFFER]
    for k in range(HORIZON):
        b_pred_meil[0, k] = min_max(b_pred_meil[0, k], valeur_avant,
                                    buffer[HEURE_POINT, T_BUFFER] + 1,
                                    min_max_seq)
        valeur_avant = b_pred_meil[0, k]

    # calcul des valeurs prévues filtrees
    b_pred_filt[0, 0] = 0.5 * buffer[FILTRE, T_BUFFER] + 0.25 * \
        b_pred_meil[0, 0] + 0.25 * b_pred_meil[0, 1]
    for k in range(1, HORIZON - 1):
        b_pred_filt[0, k] = 0.5 * b_pred_filt[0, k-1] + 0.25 * \
            b_pred_meil[0, k] + 0.25 * b_pred_meil[0, k+1]
    b_pred_filt[0, HORIZON - 1] = b_pred_meil[0, HORIZON - 1]

    # limitation des valeurs predites
    valeur_avant = buffer[NON_FILTRE, T_BUFFER]
    for k in range(HORIZON):
        b_pred_filt[0, k] = min_max(b_pred_filt[0, k], valeur_avant,
                                    buffer[HEURE_POINT, T_BUFFER] + 1,
                                    min_max_seq)
        valeur_avant = b_pred_filt[0, k]


def Apprentissage_Algorithme(ecart_pred, coef_algo, mem_pred,
                             buffer, b_pred_algo):
    """
    calcul des coefficient du meilleur predicteur a partir des predicteurs algo
    """
    vitesse = zeros((HORIZON, NB_ALGO))
    for k in range(HORIZON):

        # calcul erreur cumulee
        ecart = zeros(NB_ALGO)
        for i in range(NB_ALGO):
            for j in range(T_BUFFER-k):
                ecart[i] += abs(b_pred_algo[k+j, i, k] - buffer[NON_FILTRE,
                                                                T_BUFFER-j])
            ecart[i] /= T_BUFFER - k - 1
        rang = argsort(ecart)

        # calcul erreur pour les predicteurs retenus
        ecart_reduit = ones(NB_ALGO)*MAXI
        for i in range(NB_ALGO_REDUIT):
            ecart_reduit[rang[i]] = ecart_pred[rang[i] + I_ALGO, k]
        rang_reduit = argsort(ecart_reduit)

        # affectation des nouvelles valeurs des coef des predicteurs
        if OPTI_ALGO == 1:
            total = 0.0
            for i in range(NB_ALGO_REDUIT):
                vitesse[k, rang_reduit[i]] = 1 / \
                    max(ecart_pred[rang_reduit[i] + I_ALGO, k], 0.1)
                total += vitesse[k, rang_reduit[i]]
            for i in range(NB_ALGO_REDUIT):
                coef_algo[k, rang_reduit[i]] += vitesse[k, rang_reduit[i]] / \
                    total
        elif OPTI_ALGO == 2:
            for i in range(NB_ALGO_REDUIT):
                coef_algo[k, rang_reduit[i]] += mem_pred[i]
        else:
            coef_algo[k, rang_reduit[0]] += V_PREDIC
            coef_algo[k, rang_reduit[1]] += V_PREDIC2
            coef_algo[k, rang_reduit[2]] += V_PREDIC3

        # predicteurs supprimés
        for i in range(NB_ALGO_REDUIT, NB_ALGO):
            coef_algo[k, rang_reduit[i]] = 0.0

        # remise a 1 de la somme des predicteurs
        total = 0.0
        for i in range(NB_ALGO):
            total += coef_algo[k, i]
        for i in range(NB_ALGO):
            coef_algo[k, i] /= total
