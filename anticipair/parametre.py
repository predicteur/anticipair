# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 15:35:36 2016

@author: Philippe

Procédures liées au prédicteur par paramètre
"""

from numpy import zeros, dot, linalg

from anticipair.constante import ANNEE_POINT, HEURE_POINT, HORIZON, \
    JOUR_POINT, MAXI, MOIS_POINT, NON_FILTRE, PARA_ECART_MC, \
    PARA_HEURE, PARA_HORIZON_POINT, PRED_RESULTAT, T_BUFFER, TYPE_POINT, \
    PARA_V_VENT, V_VENT, VENT_PARANA, BUF_SERIE, BIB_SERIE
from anticipair.constante_instal import N_LIGNE
from anticipair.reference import min_max


def Predicteur_Parametre(res_param, b_pred_param, mem_param, donnees, buffer,
                         vitesse_vent, desactiv_vent, min_max_seq):
    """
    methode de prediction par parametre.
    """
    Cherche_Candidat_Parametre(res_param, mem_param, donnees, buffer)
    Traite_Candidat_Parametre(b_pred_param, donnees, buffer, res_param,
                              vitesse_vent, desactiv_vent, min_max_seq)
    return b_pred_param[0, :, :]


def Cherche_Candidat_Parametre(res_param, mem_param, donnees, buffer):
    """
    recherche de sequence dans la bibliotheque pour le prediction par parametre
    """
    AVANT = -1    # sens de recherche
    point_reference = zeros((3), dtype=int)
    point_test = zeros((3), dtype=int)

    # initialisation des candidats - resultats
    for i in range(2*PRED_RESULTAT):
        res_param[PARA_HEURE, i] = 1.0
        res_param[PARA_ECART_MC, i] = MAXI

    # initialisation des points de reference (actuel)
    Recherche_pt_carac(T_BUFFER, AVANT, point_reference, buffer)
    heure_actuel = buffer[HEURE_POINT, T_BUFFER]
    jour_actuel = buffer[JOUR_POINT, T_BUFFER]
    mois_actuel = buffer[MOIS_POINT, T_BUFFER]
    annee_actuel = buffer[ANNEE_POINT, T_BUFFER]

    # recherche sur toute la plage (sauf val courante), valeur n_test a tester
    for i in range(25):
        if donnees[HEURE_POINT, i] == buffer[HEURE_POINT, T_BUFFER]:
            n_dep = i + 24
            break
    n_total = int((N_LIGNE - n_dep) / 24)

    for h in range(n_total - 1):
        n_test = n_dep + h * 24

        # enregitrement des valeurs a tester
        Recherche_pt_carac(n_test, AVANT, point_test, donnees)
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
                ecartmc += mem_param[i] * \
                    (buffer[BUF_SERIE, point_reference[i]] -
                     donnees[BIB_SERIE, point_test[i]]) ** 2

            # resultat de 0(meilleur) a 2*PRED_RESULTAT-1(mauvais)->non utilise
            if ecartmc < res_param[PARA_ECART_MC, 2*PRED_RESULTAT-1]:
                res_param[PARA_HEURE, 2*PRED_RESULTAT - 1] = n_test
                res_param[PARA_ECART_MC, 2*PRED_RESULTAT-1] = ecartmc
            for i in range(1, 2*PRED_RESULTAT):
                if res_param[PARA_ECART_MC, 2*PRED_RESULTAT - i] < \
                        res_param[PARA_ECART_MC, 2*PRED_RESULTAT-i-1]:
                    n_bouge = res_param[PARA_HEURE, 2*PRED_RESULTAT-i]
                    ecartmc = res_param[PARA_ECART_MC, 2*PRED_RESULTAT-i]
                    res_param[PARA_HEURE, 2*PRED_RESULTAT - i] = \
                        res_param[PARA_HEURE, 2*PRED_RESULTAT-i-1]
                    res_param[PARA_ECART_MC, 2*PRED_RESULTAT - i] = \
                        res_param[PARA_ECART_MC, 2*PRED_RESULTAT-i-1]
                    res_param[PARA_HEURE, 2*PRED_RESULTAT-i-1] = n_bouge
                    res_param[PARA_ECART_MC, 2*PRED_RESULTAT-i-1] = ecartmc


def Traite_Candidat_Parametre(b_pred_param, donnees, buffer, res_param,
                              vitesse_vent, desactiv_vent, min_max_seq):
    """
    traitement des sequences trouvees pour le prediction par parametre
    """
    VAL_PT = 0    # valeur du point
    APRES = 1    # sens de recherche
    DIST_PT = 1    # distance du point
    PRED_P1 = 0    # premier point predit
    PRED_P2 = 1    # deuxieme point predit
    pt_predit = zeros((PRED_RESULTAT, 2, 2))  # 2e: info, 3e: n° futur
    pt_carac = zeros((3), dtype=int)
    spline = zeros((4))  # coef du spline

    # documentation des ecarts vv à partir de la vv au prochain point carac
    for i in range(2 * PRED_RESULTAT):
        res_param[PARA_V_VENT, i] = abs(
            donnees[V_VENT, int(res_param[PARA_HEURE, i])+HORIZON-1] -
            vitesse_vent[HORIZON - 1])

    # tri des candidats (meilleur avec 0, moins bon 2*PRED_RESULTAT-1)
    if VENT_PARANA and not desactiv_vent:
        taille = 2 * PRED_RESULTAT - 1
        ok = False
        while not ok:
            ok = True
            for i in range(taille):
                if res_param[PARA_V_VENT, i] > res_param[PARA_V_VENT, i + 1]:
                    paravvent = res_param[PARA_V_VENT, i]
                    paraheure = res_param[PARA_HEURE, i]
                    paraecartmc = res_param[PARA_ECART_MC, i]
                    res_param[PARA_V_VENT, i] = res_param[PARA_V_VENT, i + 1]
                    res_param[PARA_HEURE, i] = res_param[PARA_HEURE, i + 1]
                    res_param[PARA_ECART_MC, i] = res_param[PARA_ECART_MC, i+1]
                    res_param[PARA_V_VENT, i + 1] = paravvent
                    res_param[PARA_HEURE, i + 1] = paraheure
                    res_param[PARA_ECART_MC, i + 1] = paraecartmc
                    ok = False
            taille -= 1

    # points predits pour chaque type de resultat
    for j in range(PRED_RESULTAT):
        Recherche_pt_carac(res_param[PARA_HEURE, j], APRES, pt_carac, donnees)
        pt_predit[j, VAL_PT, PRED_P1] = donnees[BIB_SERIE, pt_carac[1]]
        pt_predit[j, VAL_PT, PRED_P2] = donnees[BIB_SERIE, pt_carac[2]]
        pt_predit[j, DIST_PT, PRED_P1] = pt_carac[1] - pt_carac[0]
        pt_predit[j, DIST_PT, PRED_P2] = pt_carac[2] - pt_carac[0]
        if j != 0:
            pt_predit[j, VAL_PT, PRED_P1] += pt_predit[j-1, VAL_PT, PRED_P1]
            pt_predit[j, VAL_PT, PRED_P2] += pt_predit[j-1, VAL_PT, PRED_P2]
            pt_predit[j, DIST_PT, PRED_P1] += pt_predit[j-1, DIST_PT, PRED_P1]
            pt_predit[j, DIST_PT, PRED_P2] += pt_predit[j-1, DIST_PT, PRED_P2]
    for j in range(PRED_RESULTAT):
        pt_predit[j, VAL_PT, PRED_P1] /= (j + 1)
        pt_predit[j, VAL_PT, PRED_P2] /= (j + 1)
        pt_predit[j, DIST_PT, PRED_P1] /= (j + 1)
        pt_predit[j, DIST_PT, PRED_P2] /= (j + 1)

    # valeurs predites avec horizon de prediction pour chaque type de resultat
    for j in range(PRED_RESULTAT):
        dist1 = pt_predit[j, DIST_PT, PRED_P1]
        dist2 = pt_predit[j, DIST_PT, PRED_P2]
        valeur1 = pt_predit[j, VAL_PT, PRED_P1]
        valeur2 = pt_predit[j, VAL_PT, PRED_P2]
        pente = (valeur1 - buffer[BUF_SERIE, T_BUFFER]) / dist1
        valeur0 = donnees[BIB_SERIE, pt_carac[0]]
        Coef_Spline(spline, valeur0, valeur1, pente, 0, dist1)
        point_dist1 = int(dist1)
        point_dist2 = int(dist2)
        for i in range(1, point_dist1+1):
            if i == HORIZON + 1:
                break
            b_pred_param[0, j, i - 1] = spline[0] + spline[1] * i + \
                spline[2] * i ** 2 + spline[3] * i ** 3
        Coef_Spline(spline, valeur1, valeur2, 0, 0, dist2 - dist1)
        for i in range(point_dist1 + 1, point_dist2 + 1):
            if i > HORIZON:
                break
            b_pred_param[0, j, i - 1] = spline[0] + spline[1] * \
                (i - point_dist1) + spline[2] * (i - point_dist1) ** 2 + \
                spline[3] * (i - point_dist1) ** 3

    # limitation des valeurs predites
    for i in range(PRED_RESULTAT):
        valeur_avant = buffer[NON_FILTRE, T_BUFFER]
        for k in range(HORIZON):
            b_pred_param[0, i, k] = min_max(b_pred_param[0, i, k],
                                            valeur_avant,
                                            buffer[HEURE_POINT, T_BUFFER] + 1,
                                            min_max_seq)
            valeur_avant = b_pred_param[0, i, k]


def Recherche_pt_carac(n_cherche, sens, pt_carac, donnee_a_traiter):
    """
    recherche de points caracteristiques d'une sequence
    dans la prediction par parametre
    """
    pt_carac[0] = n_cherche
    pt_a_trouver = 1
    for i in range(PARA_HORIZON_POINT+1):
        if donnee_a_traiter[TYPE_POINT, int(n_cherche + sens * (1 + i))] != 0:
            pt_carac[pt_a_trouver] = n_cherche + sens * (1 + i)
            if sens == 1:
                pt_a_trouver += 1
            elif abs(pt_carac[pt_a_trouver] - pt_carac[pt_a_trouver - 1]) > 2:
                pt_a_trouver += 1
        if pt_a_trouver == 3:
            break


def Coef_Spline(spline, valeur1, valeur2, pente1, pente2, dist):
    """
    generation d'une courbe spline a partir de 2 vaeurs et 2 tangentes
    """
    matrice = zeros((4, 4))
    mat_point = zeros((4, 1))

    mat_point[0, 0] = valeur1
    mat_point[1, 0] = valeur2
    mat_point[2, 0] = pente1
    mat_point[3, 0] = pente2

    matrice[0, 0] = 1.0
    matrice[1, 0] = 1.0
    matrice[2, 0] = 0.0
    matrice[3, 0] = 0.0

    matrice[0, 1] = 0.0
    matrice[1, 1] = dist
    matrice[2, 1] = 1.0
    matrice[3, 1] = 1.0

    matrice[0, 2] = 0.0
    matrice[1, 2] = dist ** 2
    matrice[2, 2] = 0.0
    matrice[3, 2] = 2 * dist

    matrice[0, 3] = 0.0
    matrice[1, 3] = dist ** 3
    matrice[2, 3] = 0.0
    matrice[3, 3] = 3 * dist ** 2

    res_mat = dot(linalg.inv(matrice), mat_point)

    for i in range(1, 5):
        spline[i - 1] = res_mat[i-1, 0]
