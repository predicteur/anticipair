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
    V_PREDIC, V_PREDIC2, V_PREDIC3, PRED_ECART, REF_SCENARIO, \
    PRED_RANG, V_VENT, I_REF, I_ANA, I_PARAM, I_VENT, I_ALGO, \
    VENT_SCENARIO, NB_ALGO, I_MEILLEUR, V_PRED_MOYEN, N_ECART, N_PREDIC, \
    N_PREDIC2, N_PREDIC3, N_MEMOIRE, N_PENAL, OPTI_ALGO, ACTIVATION_MAUVAIS, \
    ACTIVATION_VENT


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
        if valeur[VAL_VALEUR] < 0. or valeur[VAL_VALEUR] > 1000.0:
            res = -1

    return res


def AcquisitionBuffer(valeur, vitesse_vent, buffer, b_pred_meilleur):
    """
    Acquisition des valeurs du buffer a partir de valeur et vitesse_vent
    """
    # decalage d'un pas de temps des donnees : indice 0 -> la plus ancienne
    for i in range(TAILLE_BUFFER):
        buffer[NON_FILTRE, i] = buffer[NON_FILTRE, i + 1]
        buffer[HEURE_POINT, i] = buffer[HEURE_POINT, i + 1]
        buffer[FILTRE, i] = buffer[FILTRE, i + 1]
        buffer[JOUR_POINT, i] = buffer[JOUR_POINT, i + 1]
        buffer[MOIS_POINT, i] = buffer[MOIS_POINT, i + 1]
        buffer[ANNEE_POINT, i] = buffer[ANNEE_POINT, i + 1]
        buffer[V_VENT, i] = buffer[V_VENT, i + 1]
        buffer[TYPE_POINT, i] = 0
        buffer[SEQUENCE, i] = 0

    # documentation de la derniere donnee (correspond a l'instant t-1)
    buffer[V_VENT, TAILLE_BUFFER] = vitesse_vent[0]
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
        b_pred_meilleur[0, 1]
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


def Mesure_Ecart_Predicteur(ecart_predicteur, b_pred_algo, b_pred_vent,
                            b_pred_reference, b_pred_analogie,
                            b_pred_parametre, b_pred_meilleur, b_pred_filtre,
                            buffer, memoire_moyenne_ana):
    """
    Calcul de l'écart entre prediction et valeur mesurée
    """
    # ecart reel / valeurs predites avec horizon de prediction
    # pour chaque type de resultat

    for k in range(HORIZON):
        for j in range(I_REF, I_REF + REF_SCENARIO):
            ecart_predicteur[j, k] = abs(b_pred_reference[k, j-I_REF, k] -
                                         buffer[NON_FILTRE, TAILLE_BUFFER])
        for i in range(I_ANA, I_ANA + ANA_SCENARIO):
            j = round(memoire_moyenne_ana[i - I_ANA], 0)
            ecart_predicteur[i, k] = abs(b_pred_analogie[k, i-I_ANA, j, k] -
                                         buffer[NON_FILTRE, TAILLE_BUFFER])
        for j in range(I_PARAM, I_PARAM + PRED_RESULTAT):
            ecart_predicteur[j, k] = abs(b_pred_parametre[k, j-I_PARAM, k] -
                                         buffer[NON_FILTRE, TAILLE_BUFFER])
        for j in range(I_VENT, I_VENT + VENT_SCENARIO):
            ecart_predicteur[j, k] = abs(b_pred_vent[k, j-I_VENT, k] -
                                         buffer[NON_FILTRE, TAILLE_BUFFER])
        for j in range(I_ALGO, I_ALGO + NB_ALGO):
            ecart_predicteur[j, k] = abs(b_pred_algo[k, j-I_ALGO, k] -
                                         buffer[NON_FILTRE, TAILLE_BUFFER])
            #if k == 0:
            #    print('bpredalgo', k, j-I_ALGO, b_pred_algo[k, j-I_ALGO, k],
            #          buffer[NON_FILTRE, TAILLE_BUFFER], ecart_predicteur[j, k])
        ecart_predicteur[I_MEILLEUR, k] = abs(b_pred_meilleur[k, k] -
                                              buffer[NON_FILTRE,
                                                     TAILLE_BUFFER])
        ecart_predicteur[I_MEILLEUR+1, k] = abs(b_pred_filtre[k, k] -
                                                buffer[NON_FILTRE,
                                                       TAILLE_BUFFER])


def Apprentissage_Prediction(ecart_predicteur, coef_predicteur, b_pred_tableau,
                             memoire_pred, algo_param, desactiv_vent):
    """
    calcul des coeff des predicteurs algo a partir des predicteurs élémentaires
    """
    tableau = zeros((2, NB_PREDICTEURS), dtype=int)
    rang_pred = zeros((V_PRED_MOYEN + 1, NB_PREDICTEURS), dtype=int)
    rang_moyen = zeros((NB_PREDICTEURS), dtype=int)
    vitesse = zeros((HORIZON, NB_PREDICTEURS))

    for k in range(HORIZON):

        # initialisation tableau
        for i in range(REF_SCENARIO):
            b_pred_tableau[0, PRED_ECART, i+I_REF, k] = \
                ecart_predicteur[i+I_REF, k]
            b_pred_tableau[0, PRED_RANG, i+I_REF, k] = i
            if not ACTIVATION_REF:
                b_pred_tableau[0, PRED_ECART, i+I_REF, k] = MAXI
        for i in range(ANA_SCENARIO):
            b_pred_tableau[0, PRED_ECART, i + I_ANA, k] = \
                ecart_predicteur[i+I_ANA, k]
            b_pred_tableau[0, PRED_RANG, i + I_ANA, k] = \
                i + I_ANA
            if not ACTIVATION_ANA:
                b_pred_tableau[0, PRED_ECART, i+I_ANA, k] = MAXI
        for i in range(PRED_RESULTAT):
            b_pred_tableau[0, PRED_ECART, i+I_PARAM, k] = \
                ecart_predicteur[i+I_PARAM, k]
            b_pred_tableau[0, PRED_RANG, i+I_PARAM, k] = i + I_PARAM
            if not ACTIVATION_PARAM:
                b_pred_tableau[0, PRED_ECART, i+I_PARAM, k] = MAXI
        for i in range(VENT_SCENARIO):
            b_pred_tableau[0, PRED_ECART, i+I_VENT, k] = \
                ecart_predicteur[i+I_VENT, k]
            b_pred_tableau[0, PRED_RANG, i+I_VENT, k] = i + I_VENT
            if not ACTIVATION_VENT or desactiv_vent:
                b_pred_tableau[0, PRED_ECART, i+I_VENT, k] = MAXI

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
        for h in range(V_PRED_MOYEN + 1):
            for i in range(NB_PREDICTEURS):
                rang_pred[h, b_pred_tableau[h, PRED_RANG, i, k]] = i

        # lissage des rangs
        for i in range(NB_PREDICTEURS):
            rang_moyen[i] = 0
            for h in range(V_PRED_MOYEN + 1):
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
        for j in range(NB_ALGO):
            if algo_param[j, N_ECART] > 0:
                total = 0.0
                for i in range(NB_PREDICTEURS):
                    vitesse[k, i] = 1 / max(b_pred_tableau[0, PRED_ECART,
                                                           i, k], 0.01)
                    total += vitesse[k, i]
                for i in range(NB_PREDICTEURS):
                    coef_predicteur[k, i, j] += algo_param[j, N_ECART] * \
                        vitesse[k, i] / total
            elif algo_param[j, N_MEMOIRE] > 0:
                for i in range(NB_PREDICTEURS):
                    coef_predicteur[k, tableau[0, i], j] = \
                        algo_param[j, N_MEMOIRE] * \
                        coef_predicteur[k, tableau[0, i], j] + memoire_pred[i]
            else:
                coef_predicteur[k, tableau[0, 0], j] += \
                    algo_param[j, N_PREDIC]
                coef_predicteur[k, tableau[0, 1], j] += \
                    algo_param[j, N_PREDIC2]
                coef_predicteur[k, tableau[0, 2], j] += \
                    algo_param[j, N_PREDIC3]
            if algo_param[j, N_PENAL] > 0:
                coef_predicteur[k, tableau[0.0, NB_PREDICTEURS - 3], j] = \
                    max(0, coef_predicteur[k, tableau[0, NB_PREDICTEURS - 3],
                                           j] - V_PREDIC3)
                coef_predicteur[k, tableau[0.0, NB_PREDICTEURS - 2], j] = \
                    max(0, coef_predicteur[k, tableau[0, NB_PREDICTEURS - 2],
                                           j] - V_PREDIC2)
                coef_predicteur[k, tableau[0.0, NB_PREDICTEURS - 1], j] = \
                    max(0, coef_predicteur[k, tableau[0, NB_PREDICTEURS - 1],
                                           j] - V_PREDIC)

            # forcage a 0 des coef des predicteurs desactives
            if not ACTIVATION_REF:
                for i in range(REF_SCENARIO):
                    coef_predicteur[k, i + I_REF, j] = 0.0
            if not ACTIVATION_ANA:
                for i in range(ANA_SCENARIO):
                    coef_predicteur[k, i + I_ANA, j] = 0.0
            if not ACTIVATION_PARAM:
                for i in range(PRED_RESULTAT):
                    coef_predicteur[k, i + I_PARAM, j] = 0.0
            if desactiv_vent or not ACTIVATION_VENT:
                for i in range(VENT_SCENARIO):
                    coef_predicteur[k, i + I_VENT, j] = 0.0

            # remise a 1 de la somme des predicteurs
            total = 0.0
            for i in range(NB_PREDICTEURS):
                total += coef_predicteur[k, i, j]
            for i in range(NB_PREDICTEURS):
                coef_predicteur[k, i, j] /= total


def Decalage_Buffer_Pred_Meilleur(b_pred_filtre, b_pred_meilleur,
                                  b_pred_tableau):
    """
    décalage d'un pas de temps
    """
    for i in range(TAILLE_BUFFER, 0, -1):
        for l in range(HORIZON):
            b_pred_meilleur[i, l] = b_pred_meilleur[i - 1, l]
            b_pred_filtre[i, l] = b_pred_filtre[i - 1, l]
            for k in range(NB_PREDICTEURS):
                b_pred_tableau[i, 0, k, l] = b_pred_tableau[i - 1, 0, k, l]
                b_pred_tableau[i, 1, k, l] = b_pred_tableau[i - 1, 1, k, l]


def Decalage_Buffer_Pred_Algo(b_pred_algo):
    """
    décalage d'un pas de temps
    """
    for i in range(TAILLE_BUFFER, 0, -1):
        for k in range(NB_ALGO):
            for l in range(HORIZON):
                b_pred_algo[i, k, l] = b_pred_algo[i - 1, k, l]


def Meilleure_Prediction(b_pred_algo, b_pred_filtre, b_pred_vent,
                         b_pred_meilleur, b_pred_reference, b_pred_analogie,
                         b_pred_parametre, coef_algo, coef_predicteur,
                         memoire_moyenne_ana, buffer):
    """
    calcul des prediction algo a partir des predicteurs elementaires
    """
    # calcul des valeurs prévues par algorithme
    for l in range(NB_ALGO):
        for k in range(HORIZON):
            b_pred_algo[0, l, k] = 0.0

            # valeur de reference
            for i in range(REF_SCENARIO):
                b_pred_algo[0, l, k] += coef_predicteur[k, i, l] * \
                    b_pred_reference[0, i, k]

            # valeur de predicteur analogie
            for i in range(ANA_SCENARIO):
                j = round(memoire_moyenne_ana[i], 0)
                b_pred_algo[0, l, k] += coef_predicteur[k, i + I_ANA, l] * \
                    b_pred_analogie[0, i, j, k]

            # valeur de predicteur parametre
            for i in range(PRED_RESULTAT):
                b_pred_algo[0, l, k] += coef_predicteur[k, i + I_PARAM, l] * \
                    b_pred_parametre[0, i, k]

            # valeur de predicteur correlation vent
            for i in range(VENT_SCENARIO):
                b_pred_algo[0, l, k] += coef_predicteur[k, i + I_VENT, l] * \
                    b_pred_vent[0, i, k]

    # calcul des meilleures valeurs prevues
    for k in range(HORIZON):
        b_pred_meilleur[0, k] = 0.0
        for i in range(NB_ALGO):
            b_pred_meilleur[0, k] += (coef_algo[k, i] * b_pred_algo[0, i, k])

    # calcul des valeurs prévues filtrees
    b_pred_filtre[0, 0] = 0.5 * buffer[FILTRE, TAILLE_BUFFER] + 0.25 * \
        b_pred_meilleur[0, 0] + 0.25 * b_pred_meilleur[0, 1]
    for k in range(1, HORIZON - 1):
        b_pred_filtre[0, k] = 0.5 * b_pred_filtre[0, k-1] + 0.25 * \
            b_pred_meilleur[0, k] + 0.25 * b_pred_meilleur[0, k+1]
    b_pred_filtre[0, HORIZON - 1] = b_pred_meilleur[0, HORIZON - 1]


def Apprentissage_Algorithme(ecart_predicteur, coef_algo, memoire_pred):
    """
    calcul des coefficient du meilleur predicteur a partir des predicteurs algo
    """
    tableau = zeros((2, NB_ALGO, HORIZON))
    vitesse = zeros((HORIZON, NB_ALGO))

    for k in range(HORIZON):

        # initialisation tableau
        for i in range(NB_ALGO):
            tableau[PRED_ECART, i, k] = ecart_predicteur[i + I_ALGO, k]
            tableau[PRED_RANG, i, k] = i

        # tri tableau (meilleur avec 0, moins bon NB_ALGO-1)
        taille = NB_ALGO - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if tableau[PRED_ECART, i, k] > tableau[PRED_ECART, i + 1, k]:
                    interval = tableau[PRED_ECART, i, k]
                    interrang = tableau[PRED_RANG, i, k]
                    tableau[PRED_ECART, i, k] = tableau[PRED_ECART, i + 1, k]
                    tableau[PRED_RANG, i, k] = tableau[PRED_RANG, i + 1, k]
                    tableau[PRED_ECART, i + 1, k] = interval
                    tableau[PRED_RANG, i + 1, k] = interrang
                    ok = False
            taille = taille - 1

        # affectation des nouvelles valeurs des coef des predicteurs
        if OPTI_ALGO == 1:
            total = 0.0
            for i in range(NB_ALGO):
                vitesse[k, i] = 1 / max(ecart_predicteur[i + I_ALGO, k], 0.1)
                total += vitesse[k, i]
            for i in range(NB_ALGO):
                coef_algo[k, i] += vitesse[k, i] / total
        elif OPTI_ALGO == 2:
            for i in range(NB_ALGO):
                coef_algo[k, tableau[PRED_RANG, i, k]] += memoire_pred[i]
        else:
            coef_algo[k, tableau[PRED_RANG, 0, k]] += V_PREDIC
            coef_algo[k, tableau[PRED_RANG, 1, k]] += V_PREDIC2
            coef_algo[k, tableau[PRED_RANG, 2, k]] += V_PREDIC3
        if ACTIVATION_MAUVAIS:
            coef_algo[k, tableau[PRED_RANG, NB_ALGO - 3, k]] = \
                max(0, coef_algo[k, tableau[PRED_RANG, NB_ALGO - 3, k]] -
                    V_PREDIC3)
            coef_algo[k, tableau[PRED_RANG, NB_ALGO - 2, k]] = \
                max(0, coef_algo[k, tableau[PRED_RANG, NB_ALGO - 2, k]] -
                    V_PREDIC2)
            coef_algo[k, tableau[PRED_RANG, NB_ALGO - 1, k]] = \
                max(0, coef_algo[k, tableau[PRED_RANG, NB_ALGO - 1, k]] -
                    V_PREDIC)

        # remise a 1 de la somme des predicteurs
        total = 0.0
        for i in range(NB_ALGO):
            total += coef_algo[k, i]
        for i in range(NB_ALGO):
            coef_algo[k, i] /= total
