# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:32:14 2016

@author: Philippe

Procédures du prédicteur par analogie

"""

from numpy import zeros
from math import sqrt
from constante import ANA_ECART_MC, ANA_FILTRAGE, ANA_FILTRAGE_BIBLIO, \
    ANA_HEURE, ANA_PROFONDEUR, ANA_SCENARIO, ANNEE_POINT, FILTRE, HEURE_POINT,\
    HORIZON, JOUR_POINT, MAXI, MOIS_POINT, NON_FILTRE, N_LIGNE, PRED_RESULTAT,\
    TAILLE_BUFFER, V_MOYENNE


def Mesure_Ecart_Analogie(ecart_pred_analogie, b_prediction_analogie,
                          ecart_analogie_global, horizon_pred, buffer):

    # ecart reel / valeurs predites avec horizon de prediction pour chaque
    # type de resultat
    for i in range(ANA_SCENARIO):
        for j in range(PRED_RESULTAT):
            for k in range(HORIZON):
                ecart_pred_analogie[i, j, k] = \
                    abs(b_prediction_analogie[k, i, j, k] -
                        buffer[NON_FILTRE, TAILLE_BUFFER])

    # ecart complet sur l horizon de prediction pour chaque type de resultat
    for i in range(ANA_SCENARIO):
        for j in range(PRED_RESULTAT):
            ecart_analogie_global[i, j] = 0
            for k in range(HORIZON):
                ecart_analogie_global[i, j] += horizon_pred[k] * \
                    ecart_pred_analogie[i, j, k] ** 2
            ecart_analogie_global[i, j] = sqrt(ecart_analogie_global[i, j])


def Apprentissage_Analogie(ecart_analogie_global, memoire_moyenne_ana):

    for i in range(ANA_SCENARIO):

        meilleur = 0
        meilleure_valeur = MAXI
        for j in range(PRED_RESULTAT):
            if ecart_analogie_global[i, j] < meilleure_valeur:
                meilleur = j
                meilleure_valeur = ecart_analogie_global[i, j]
        memoire_moyenne_ana[i] += V_MOYENNE * \
            (meilleur - memoire_moyenne_ana[i])


def Decalage_Buffer_Pred_Analogie(b_prediction_analogie):

    for i in range(TAILLE_BUFFER, 0, -1):
        for j in range(ANA_SCENARIO):
            for k in range(PRED_RESULTAT):
                for l in range(HORIZON):
                    b_prediction_analogie[i, j, k, l] = \
                        b_prediction_analogie[i - 1, j, k, l]


def Predicteur_Analogie(resultat_analogie, b_prediction_analogie,
                        memoire_analogie, donnees, buffer):

    for j in range(ANA_SCENARIO):
        Cherche_Candidat_Analogie(j, resultat_analogie, memoire_analogie,
                                  donnees, buffer)
        Traite_Candidat_Analogie(j, b_prediction_analogie, resultat_analogie,
                                 donnees)


def Cherche_Candidat_Analogie(n_sce, resultat_analogie, memoire_analogie,
                              donnees, buffer):

    actuel = zeros((ANA_PROFONDEUR))
    cas_test = zeros((ANA_PROFONDEUR))

    # initialisation des candidats - resultats
    for i in range(PRED_RESULTAT):
        resultat_analogie[ANA_HEURE, i] = 1
        resultat_analogie[ANA_ECART_MC, i] = MAXI

    # initialisation des valeurs de reference (actuel)
    for i in range(ANA_PROFONDEUR):
        if ANA_FILTRAGE:
            actuel[i] = buffer[FILTRE, TAILLE_BUFFER+1-ANA_PROFONDEUR+i]
        else:
            actuel[i] = buffer[NON_FILTRE, TAILLE_BUFFER+1-ANA_PROFONDEUR+i]
    heure_actuel = buffer[HEURE_POINT, TAILLE_BUFFER]
    jour_actuel = buffer[JOUR_POINT, TAILLE_BUFFER]
    mois_actuel = buffer[MOIS_POINT, TAILLE_BUFFER]
    annee_actuel = buffer[ANNEE_POINT, TAILLE_BUFFER]

    # synchronisation sur l'heure des donnees a tester (sauf valeur courante)
    for i in range(25):
        if donnees[HEURE_POINT, i] == buffer[HEURE_POINT, TAILLE_BUFFER]:
            n_dep = i + 24
            break
    n_total = int((N_LIGNE - n_dep) / 24)
    for h in range(n_total-1):
        n_test = n_dep + h * 24

        # enregitrement des valeurs a tester
        for i in range(ANA_PROFONDEUR):
            if ANA_FILTRAGE_BIBLIO:
                cas_test[i] = donnees[FILTRE, n_test-ANA_PROFONDEUR+i+1]
            else:
                cas_test[i] = donnees[NON_FILTRE, n_test-ANA_PROFONDEUR+i+1]
        heure_test = donnees[HEURE_POINT, n_test]
        jour_test = donnees[JOUR_POINT, n_test]
        mois_test = donnees[MOIS_POINT, n_test]
        annee_test = donnees[ANNEE_POINT, n_test]

        # calcul de l'ecart
        if abs(heure_test-heure_actuel) + abs(jour_test-jour_actuel) +\
                abs(mois_test-mois_actuel) + abs(annee_test-annee_actuel) >\
                0.5:
            ecartmc = 0.
            for i in range(ANA_PROFONDEUR):
                ecartmc += memoire_analogie[i, n_sce] * \
                    (cas_test[i] - actuel[i]) ** 2

            # if n_test == 15461 and n_sce == 6:
                # print("ecartmc15461, n_sce", ecartmc, n_sce)
                # for i in range(ANA_PROFONDEUR):
                # print("mem-ana, cas-test, actuel",
                # memoire_analogie[i, n_sce], cas_test[i], actuel[i])

            # res_analogie de 0(meilleur) a resultat-1(mauvais)->non utilise!
            if ecartmc < resultat_analogie[ANA_ECART_MC, PRED_RESULTAT - 1]:
                resultat_analogie[ANA_HEURE, PRED_RESULTAT-1] = n_test
                resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-1] = ecartmc
            for i in range(1, PRED_RESULTAT):
                if resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i] < \
                       resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i-1]:
                    n_bouge = resultat_analogie[ANA_HEURE, PRED_RESULTAT-i]
                    ecartmc = resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i]
                    resultat_analogie[ANA_HEURE, PRED_RESULTAT-i] = \
                        resultat_analogie[ANA_HEURE, PRED_RESULTAT-i-1]
                    resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i] = \
                        resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i-1]
                    resultat_analogie[ANA_HEURE, PRED_RESULTAT-i-1] = n_bouge
                    resultat_analogie[ANA_ECART_MC, PRED_RESULTAT-i-1] = \
                        ecartmc


def Traite_Candidat_Analogie(n_sce, b_prediction_analogie, resultat_analogie,
                             donnees):

    # type filtrage utilise
    if ANA_FILTRAGE:
        filtre_o_n = FILTRE
    else:
        filtre_o_n = NON_FILTRE

    # valeurs predites avec horizon de prediction pour chaque type de resultat
    for k in range(HORIZON):
        b_prediction_analogie[0, n_sce, 0, k] = \
            donnees[filtre_o_n, resultat_analogie[ANA_HEURE, 0]+1+k]
        for j in range(1, PRED_RESULTAT):
            b_prediction_analogie[0, n_sce, j, k] = \
                b_prediction_analogie[0, n_sce, j-1, k] + \
                donnees[filtre_o_n, resultat_analogie[ANA_HEURE, j]+1+k]
        for j in range(PRED_RESULTAT):
            b_prediction_analogie[0, n_sce, j, k] /= (j+1)

    # if n_sce == 6:
        # for j in range(5):
            # print("b_pred_ana", j, b_prediction_analogie[0, n_sce, j, 0], )
            # print("res_ana et mc", resultat_analogie[ANA_HEURE, j],
            # resultat_analogie[ANA_ECART_MC, j])
