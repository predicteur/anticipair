# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:35:36 2016

@author: Philippe

Procédures liées au prédicteur par paramètre
"""

from numpy import zeros, dot, linalg
from constante import ANNEE_POINT, HEURE_POINT, HORIZON, \
    JOUR_POINT, MAXI, MOIS_POINT, NON_FILTRE, N_LIGNE, PARA_ECART_MC, \
    PARA_HEURE, PARA_HORIZON_POINT, PRED_RESULTAT, TAILLE_BUFFER, TYPE_POINT, \
    PARA_V_VENT, V_VENT, VENT_PARANA


def Mesure_Ecart_Parametre(ecart_pred_parametre, b_pred_parametre,
                           horizon_pred, buffer):

    # ecart reel / valeurs predites avec horizon de prediction
    # pour chaque type de resultat

    for j in range(PRED_RESULTAT):
        for k in range(HORIZON):
            ecart_pred_parametre[j, k] = \
                abs(b_pred_parametre[k, j, k] -
                    buffer[NON_FILTRE, TAILLE_BUFFER])


def Decalage_Buffer_Pred_Parametre(b_pred_parametre):

    for i in range(TAILLE_BUFFER, 0, -1):
        for k in range(PRED_RESULTAT):
            for l in range(HORIZON):
                b_pred_parametre[i, k, l] = b_pred_parametre[i - 1, k, l]


def Predicteur_Parametre(resultat_parametre, b_pred_parametre,
                         memoire_param, donnees, buffer, vitesse_vent,
                         desactiv_vent):

    Cherche_Candidat_Parametre(resultat_parametre, memoire_param, donnees,
                               buffer)
    Traite_Candidat_Parametre(b_pred_parametre, donnees, buffer,
                              resultat_parametre, vitesse_vent, desactiv_vent)


def Cherche_Candidat_Parametre(resultat_parametre, memoire_param, donnees,
                               buffer):

    AVANT = -1    # sens de recherche
    point_reference = zeros((3), dtype=int)
    point_test = zeros((3), dtype=int)

    # initialisation des candidats - resultats
    for i in range(2*PRED_RESULTAT):
        resultat_parametre[PARA_HEURE, i] = 1
        resultat_parametre[PARA_ECART_MC, i] = MAXI

    # initialisation des points de reference (actuel)
    Recherche_Point_Carac(TAILLE_BUFFER, AVANT, point_reference, buffer)
    heure_actuel = buffer[HEURE_POINT, TAILLE_BUFFER]
    jour_actuel = buffer[JOUR_POINT, TAILLE_BUFFER]
    mois_actuel = buffer[MOIS_POINT, TAILLE_BUFFER]
    annee_actuel = buffer[ANNEE_POINT, TAILLE_BUFFER]

    # recherche sur toute la plage (sauf val courante), valeur n_test a tester
    for i in range(25):
        if donnees[HEURE_POINT, i] == buffer[HEURE_POINT, TAILLE_BUFFER]:
            n_dep = i + 24
            break
    n_total = int((N_LIGNE - n_dep) / 24)

    for h in range(n_total - 1):
        n_test = n_dep + h * 24

        # enregitrement des valeurs a tester
        Recherche_Point_Carac(n_test, AVANT, point_test, donnees)
        heure_test = donnees[HEURE_POINT, n_test]
        jour_test = donnees[JOUR_POINT, n_test]
        mois_test = donnees[MOIS_POINT, n_test]
        annee_test = donnees[ANNEE_POINT, n_test]

        # calcul de l'ecart
        if abs(heure_test-heure_actuel) + abs(jour_test-jour_actuel) + \
                abs(mois_test-mois_actuel) + abs(annee_test-annee_actuel) > \
                0.5:
            ecartmc = 0
            for i in range(3):
                ecartmc += memoire_param[i] * \
                    (buffer[NON_FILTRE, point_reference[i]] -
                     donnees[NON_FILTRE, point_test[i]]) ** 2

            # resultat de 0(meilleur) a 2*PRED_RESULTAT-1(mauvais)->non utilise
            if ecartmc < resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-1]:
                resultat_parametre[PARA_HEURE, 2*PRED_RESULTAT - 1] = n_test
                resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-1] = ecartmc
            for i in range(1, 2*PRED_RESULTAT):
                if resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT - i] < \
                        resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-i-1]:
                    n_bouge = resultat_parametre[PARA_HEURE, 2*PRED_RESULTAT-i]
                    ecartmc = \
                        resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-i]
                    resultat_parametre[PARA_HEURE, 2*PRED_RESULTAT - i] = \
                        resultat_parametre[PARA_HEURE, 2*PRED_RESULTAT-i-1]
                    resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT - i] = \
                        resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-i-1]
                    resultat_parametre[PARA_HEURE, 2*PRED_RESULTAT-i-1] = \
                        n_bouge
                    resultat_parametre[PARA_ECART_MC, 2*PRED_RESULTAT-i-1] = \
                        ecartmc


def Traite_Candidat_Parametre(b_pred_parametre, donnees, buffer,
                              resultat_parametre, vitesse_vent, desactiv_vent):

    VALEUR_M_POINT = 0    # valeur du point
    APRES = 1    # sens de recherche
    DIST_M_POINT = 1    # distance du point
    PRED_P1 = 0    # premier point predit
    PRED_P2 = 1    # deuxieme point predit
    point_predit = zeros((PRED_RESULTAT, 2, 2))  # 2e: info, 3e: n° futur
    point_carac = zeros((3), dtype=int)
    spline = zeros((4))  # coef du spline

    # documentation des ecarts vv à partir de la vv au prochain point carac
    for i in range(2 * PRED_RESULTAT):
        resultat_parametre[PARA_V_VENT, i] = \
            abs(donnees[V_VENT, resultat_parametre[PARA_HEURE, i] +
                HORIZON - 1] - vitesse_vent[HORIZON - 1])

    # tri des candidats (meilleur avec 0, moins bon 2*PRED_RESULTAT-1)
    if VENT_PARANA and not desactiv_vent:
        taille = 2 * PRED_RESULTAT - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if resultat_parametre[PARA_V_VENT, i] > \
                        resultat_parametre[PARA_V_VENT, i + 1]:
                    paravvent = resultat_parametre[PARA_V_VENT, i]
                    paraheure = resultat_parametre[PARA_HEURE, i]
                    paraecartmc = resultat_parametre[PARA_ECART_MC, i]
                    resultat_parametre[PARA_V_VENT, i] = \
                        resultat_parametre[PARA_V_VENT, i + 1]
                    resultat_parametre[PARA_HEURE, i] = \
                        resultat_parametre[PARA_HEURE, i + 1]
                    resultat_parametre[PARA_ECART_MC, i] = \
                        resultat_parametre[PARA_ECART_MC, i + 1]
                    resultat_parametre[PARA_V_VENT, i + 1] = paravvent
                    resultat_parametre[PARA_HEURE, i + 1] = paraheure
                    resultat_parametre[PARA_ECART_MC, i + 1] = paraecartmc
                    ok = False
            taille -= 1

    # points predits pour chaque type de resultat
    for j in range(PRED_RESULTAT):
        Recherche_Point_Carac(resultat_parametre[PARA_HEURE, j], APRES,
                              point_carac, donnees)
        point_predit[j, VALEUR_M_POINT, PRED_P1] = \
            donnees[NON_FILTRE, point_carac[1]]
        point_predit[j, VALEUR_M_POINT, PRED_P2] = \
            donnees[NON_FILTRE, point_carac[2]]
        point_predit[j, DIST_M_POINT, PRED_P1] = \
            point_carac[1] - point_carac[0]
        point_predit[j, DIST_M_POINT, PRED_P2] = \
            point_carac[2] - point_carac[0]
        if j != 0:
            point_predit[j, VALEUR_M_POINT, PRED_P1] += \
                point_predit[j-1, VALEUR_M_POINT, PRED_P1]
            point_predit[j, VALEUR_M_POINT, PRED_P2] += \
                point_predit[j-1, VALEUR_M_POINT, PRED_P2]
            point_predit[j, DIST_M_POINT, PRED_P1] += \
                point_predit[j - 1, DIST_M_POINT, PRED_P1]
            point_predit[j, DIST_M_POINT, PRED_P2] += \
                point_predit[j - 1, DIST_M_POINT, PRED_P2]
    for j in range(PRED_RESULTAT):
            point_predit[j, VALEUR_M_POINT, PRED_P1] /= (j + 1)
            point_predit[j, VALEUR_M_POINT, PRED_P2] /= (j + 1)
            point_predit[j, DIST_M_POINT, PRED_P1] /= (j + 1)
            point_predit[j, DIST_M_POINT, PRED_P2] /= (j + 1)

    # valeurs predites avec horizon de prediction pour chaque type de resultat
    for j in range(PRED_RESULTAT):
        dist1 = point_predit[j, DIST_M_POINT, PRED_P1]
        dist2 = point_predit[j, DIST_M_POINT, PRED_P2]
        valeur1 = point_predit[j, VALEUR_M_POINT, PRED_P1]
        valeur2 = point_predit[j, VALEUR_M_POINT, PRED_P2]
        pente = (valeur1 - buffer[NON_FILTRE, TAILLE_BUFFER]) / dist1
        valeur0 = donnees[NON_FILTRE, point_carac[0]]
        Coef_Spline(spline, valeur0, valeur1, pente, 0, dist1)
        point_dist1 = int(dist1)
        point_dist2 = int(dist2)
        for i in range(1, point_dist1+1):
            if i == HORIZON + 1:
                break
            b_pred_parametre[0, j, i - 1] = spline[0] + spline[1] * i + \
                spline[2] * i ** 2 + spline[3] * i ** 3
        Coef_Spline(spline, valeur1, valeur2, 0, 0, dist2 - dist1)
        for i in range(point_dist1 + 1, point_dist2 + 1):
            if i > HORIZON:
                break
            b_pred_parametre[0, j, i - 1] = spline[0] + spline[1] * \
                (i - point_dist1) + spline[2] * (i - point_dist1) ** 2 + \
                spline[3] * (i - point_dist1) ** 3


def Recherche_Point_Carac(n_cherche, sens, point_carac, donnee_a_traiter):

    point_carac[0] = n_cherche
    point_a_trouver = 1
    for i in range(PARA_HORIZON_POINT+1):
        if donnee_a_traiter[TYPE_POINT, n_cherche + sens * (1 + i)] != 0:
            point_carac[point_a_trouver] = n_cherche + sens * (1 + i)
            if sens == 1:
                point_a_trouver = point_a_trouver + 1
            elif abs(point_carac[point_a_trouver] -
                     point_carac[point_a_trouver - 1]) > 2:
                        point_a_trouver = point_a_trouver + 1
        if point_a_trouver == 3:
            break


def Coef_Spline(spline, valeur1, valeur2, pente1, pente2, dist):

    matrice = zeros((4, 4))
    mat_point = zeros((4, 1))

    mat_point[0, 0] = valeur1
    mat_point[1, 0] = valeur2
    mat_point[2, 0] = pente1
    mat_point[3, 0] = pente2

    matrice[0, 0] = 1
    matrice[1, 0] = 1
    matrice[2, 0] = 0
    matrice[3, 0] = 0

    matrice[0, 1] = 0
    matrice[1, 1] = dist
    matrice[2, 1] = 1
    matrice[3, 1] = 1

    matrice[0, 2] = 0
    matrice[1, 2] = dist ** 2
    matrice[2, 2] = 0
    matrice[3, 2] = 2 * dist

    matrice[0, 3] = 0
    matrice[1, 3] = dist ** 3
    matrice[2, 3] = 0
    matrice[3, 3] = 3 * dist ** 2

    res_mat = dot(linalg.inv(matrice), mat_point)

    for i in range(1, 5):
        spline[i - 1] = res_mat[i-1, 0]
