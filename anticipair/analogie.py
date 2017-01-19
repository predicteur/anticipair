# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:32:14 2016

@author: Philippe

Procédures du prédicteur par analogie

"""

from math import sqrt

from numpy import zeros

from anticipair.constante import ANA_ECART_MC, ANA_HEURE, ANA_PROFONDEUR, ANA_SCENARIO, \
    ANNEE_POINT, HEURE_POINT, HORIZON, JOUR_POINT, MAXI, MOIS_POINT, \
    PRED_RESULTAT, T_BUFFER, V_MOYENNE, ANA_V_VENT, V_VENT, VENT_PARANA, \
    BUF_SERIE, BIB_SERIE, NON_FILTRE
from anticipair.constante_instal import N_LIGNE
from anticipair.reference import min_max


def Apprentissage_Analogie(h_pred, b_pred_ana, mem_moy_ana, buffer):
    """
    Procédure d apprentissage specifique du prédicteur par analogie
    """
    ecart_pred_ana = zeros((ANA_SCENARIO, PRED_RESULTAT, HORIZON))
    ecart_ana_gl = zeros((ANA_SCENARIO, PRED_RESULTAT))

    # ecart reel / predites avec horizon de pred pour chaque type de resultat
    for i in range(ANA_SCENARIO):
        for j in range(PRED_RESULTAT):
            for k in range(HORIZON):
                ecart_pred_ana[i, j, k] = \
                    abs(b_pred_ana[k, i, j, k] - buffer[NON_FILTRE, T_BUFFER])

    # ecart complet sur l horizon de prediction pour chaque type de resultat
    for i in range(ANA_SCENARIO):
        for j in range(PRED_RESULTAT):
            ecart_ana_gl[i, j] = 0.0
            for k in range(HORIZON):
                ecart_ana_gl[i, j] += h_pred[k] * ecart_pred_ana[i, j, k] ** 2
            ecart_ana_gl[i, j] = sqrt(ecart_ana_gl[i, j])

    # calcul de la meilleure moyenne
    for i in range(ANA_SCENARIO):
        meilleur = 0.0
        meilleure_valeur = MAXI
        for j in range(PRED_RESULTAT):
            if ecart_ana_gl[i, j] < meilleure_valeur:
                meilleur = j
                meilleure_valeur = ecart_ana_gl[i, j]
        mem_moy_ana[i] += V_MOYENNE * (meilleur - mem_moy_ana[i])


def Predicteur_Analogie(res_ana, b_pred_ana,
                        mem_ana, donnees, buffer, vitesse_vent,
                        desactiv_vent, mem_moy_ana, min_max_seq):
    """
    methode de prediction par analogie.
    """
    b_pred_reduit = zeros((T_BUFFER+1, ANA_SCENARIO, HORIZON))
    for j in range(ANA_SCENARIO):
        Cherche_Candidat_Analogie(j, res_ana, mem_ana, donnees, buffer)
        Traite_Candidat_Analogie(j, b_pred_ana, res_ana, donnees,
                                 vitesse_vent, desactiv_vent)
        for k in range(HORIZON):
            i = int(round(mem_moy_ana[j], 0))
            b_pred_reduit[0, j, k] = b_pred_ana[0, j, i, k]

    # limitation des valeurs predites
    for i in range(ANA_SCENARIO):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_reduit[0, i, k] = \
                min_max(b_pred_reduit[0, i, k], valeur_avant,
                        buffer[HEURE_POINT, T_BUFFER] + 1, min_max_seq)
            valeur_avant = b_pred_reduit[0, i, k]

    return b_pred_reduit[0, :, :]


def Cherche_Candidat_Analogie(n_sce, res_ana, mem_ana,
                              donnees, buffer):
    """
    recherche de sequence dans la bibliotheque pour le prediction par analogie
    """
    actuel = zeros((ANA_PROFONDEUR))
    cas_test = zeros((ANA_PROFONDEUR))

    # initialisation des candidats - resultats
    for i in range(2 * PRED_RESULTAT):
        res_ana[ANA_HEURE, i] = 1.0
        res_ana[ANA_ECART_MC, i] = MAXI
        res_ana[ANA_V_VENT, i] = 0.0

    # initialisation des valeurs de reference (actuel)
    for i in range(ANA_PROFONDEUR):
        actuel[i] = buffer[BUF_SERIE, T_BUFFER+1-ANA_PROFONDEUR+i]
    heure_actuel = buffer[HEURE_POINT, T_BUFFER]
    jour_actuel = buffer[JOUR_POINT, T_BUFFER]
    mois_actuel = buffer[MOIS_POINT, T_BUFFER]
    annee_actuel = buffer[ANNEE_POINT, T_BUFFER]

    # synchronisation sur l'heure des donnees a tester (sauf valeur courante)
    for i in range(25):
        if donnees[HEURE_POINT, i] == buffer[HEURE_POINT, T_BUFFER]:
            n_dep = i + 24
            break
    n_total = int((N_LIGNE - n_dep) / 24)
    for h in range(n_total-1):
        n_test = n_dep + h * 24

        # enregitrement des valeurs a tester
        for i in range(ANA_PROFONDEUR):
            cas_test[i] = donnees[BIB_SERIE, n_test-ANA_PROFONDEUR+i+1]
        heure_test = donnees[HEURE_POINT, n_test]
        jour_test = donnees[JOUR_POINT, n_test]
        mois_test = donnees[MOIS_POINT, n_test]
        annee_test = donnees[ANNEE_POINT, n_test]

        # calcul de l'ecart
        if abs(heure_test-heure_actuel) + abs(jour_test-jour_actuel) +\
                abs(mois_test-mois_actuel) + abs(annee_test-annee_actuel) >\
                0.5:
            ecartmc = 0.0
            for i in range(ANA_PROFONDEUR):
                ecartmc += mem_ana[i, n_sce] * (cas_test[i] - actuel[i]) ** 2

            # res_analogie de 0(meilleur) a 2*resultat-1(mauvais)->non utilise!
            if ecartmc < res_ana[ANA_ECART_MC, 2*PRED_RESULTAT - 1]:
                res_ana[ANA_HEURE, 2*PRED_RESULTAT-1] = n_test
                res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-1] = ecartmc
            for i in range(1, 2*PRED_RESULTAT):
                if res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i] < \
                       res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i-1]:
                    n_bouge = res_ana[ANA_HEURE, 2*PRED_RESULTAT-i]
                    ecartmc = res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i]
                    res_ana[ANA_HEURE, 2*PRED_RESULTAT-i] = \
                        res_ana[ANA_HEURE, 2*PRED_RESULTAT-i-1]
                    res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i] = \
                        res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i-1]
                    res_ana[ANA_HEURE, 2*PRED_RESULTAT-i-1] = n_bouge
                    res_ana[ANA_ECART_MC, 2*PRED_RESULTAT-i-1] = ecartmc


def Traite_Candidat_Analogie(n_sce, b_pred_ana, res_ana, donnees,
                             vitesse_vent, desactiv_vent):
    """
    traitement des sequences trouvees pour le predicteur par analogie
    """
    for k in range(HORIZON):

        # documentation des ecarts vv
        for i in range(2 * PRED_RESULTAT):
            res_ana[ANA_V_VENT, i] = \
                abs(donnees[V_VENT, int(res_ana[ANA_HEURE, i])+k+1] -
                    vitesse_vent[k+1])

        # tri des candidats (meilleur avec 0, moins bon 2*PRED_RESULTAT-1)
        if VENT_PARANA and not desactiv_vent and donnees[V_VENT, 1] > -0.5:
            taille = 2 * PRED_RESULTAT - 1
            ok = False
            while not ok:
                ok = True
                for i in range(taille):
                    if res_ana[ANA_V_VENT, i] > res_ana[ANA_V_VENT, i + 1]:
                        anavvent = res_ana[ANA_V_VENT, i]
                        anaheure = res_ana[ANA_HEURE, i]
                        anaecartmc = res_ana[ANA_ECART_MC, i]
                        res_ana[ANA_V_VENT, i] = res_ana[ANA_V_VENT, i + 1]
                        res_ana[ANA_HEURE, i] = res_ana[ANA_HEURE, i + 1]
                        res_ana[ANA_ECART_MC, i] = res_ana[ANA_ECART_MC, i + 1]
                        res_ana[ANA_V_VENT, i + 1] = anavvent
                        res_ana[ANA_HEURE, i + 1] = anaheure
                        res_ana[ANA_ECART_MC, i + 1] = anaecartmc
                        ok = False
                taille -= 1

        # valeurs predites avec horizon de pred pour chaque type de resultat
        b_pred_ana[0, n_sce, 0, k] = donnees[BUF_SERIE,
                                             int(res_ana[ANA_HEURE, 0])+1+k]
        for j in range(1, PRED_RESULTAT):
            b_pred_ana[0, n_sce, j, k] = b_pred_ana[0, n_sce, j-1, k] + \
                donnees[BUF_SERIE, int(res_ana[ANA_HEURE, j])+1+k]
        for j in range(PRED_RESULTAT):
            b_pred_ana[0, n_sce, j, k] /= (j+1)
