# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 13:19:04 2016

@author: Philippe

Affichage des valeurs intermédiaires pour debug (console et/ou fichier)
"""

from anticipair.constante import ANA_SCENARIO, FILTRE, HEURE_POINT, \
    HORIZON, NB_PREDICTEURS, NON_FILTRE, PRED_RESULTAT, SEQUENCE, \
    T_BUFFER, TYPE_POINT, VENT_SCENARIO, NB_ALGO, REF_SCENARIO, \
    I_ANA, I_PARAM, I_MEILLEUR, I_REF, I_VENT, I_ALGO, \
    AFFICHE_HORIZON, V_PREDIC, V_PREDIC2, V_PREDIC3, V_MOYENNE, \
    ANA_PROFONDEUR, BUF_SERIE, BIB_SERIE, PARA_PROFONDEUR, \
    PARA_HORIZON_POINT, PARA_SENS, VENT_MIN, VENT_MAX, VENT_PRED,\
    VENT_PARANA, REF_PENTE, V_PRED_MOYEN, V_PENAL, V_MEMOIRE, V_ECART, \
    ACTIVATION_REF, ACTIVATION_ANA, ACTIVATION_PARAM, ACTIVATION_VENT, \
    ACTIVATION_MAUVAIS, OPTI_ALGO, I_MODELE, MODELE_SCENARIO, \
    ACTIVATION_MODELE, NB_PRED_REDUIT, NB_ALGO_REDUIT, MAX_VARIATION, \
    MAX_VALEUR, ECRETE
from anticipair.constante_instal import N_LIGNE, FILE_BIBLIO


def Affiche_Donnees_Traitees(donnees):
    """
    affichage de la bibliotheque
    """
    print("heure", "non-filtre", "sequence", "type_point", "filtre")
    # for i in range(1, 10):
    for i in range(6184, 6204):
        print(donnees[HEURE_POINT, i], donnees[NON_FILTRE, i],
              donnees[SEQUENCE, i], donnees[TYPE_POINT, i],
              donnees[FILTRE, i])
    print(donnees[HEURE_POINT, N_LIGNE - 1], donnees[NON_FILTRE, N_LIGNE - 1],
          donnees[SEQUENCE, N_LIGNE - 1], donnees[TYPE_POINT, N_LIGNE - 1],
          donnees[FILTRE, N_LIGNE - 1])


def Affiche_Buffer(buffer):
    """
    affichage du buffer
    """
    print("non filtre", "filtre", "sequence", "type_point", "heure", "jour",
          "mois", "annee", "vent", "modele")
    print(buffer)


def Affiche_Analogie(buffer, b_pred_ana, ecart_pred):
    """
    affichage du predicteur analogie
    """
    i = 6
    k = AFFICHE_HORIZON
    print("b_pred-ana0600", "b_pred_ana0640",
          b_pred_ana[k, i, 0, k], b_pred_ana[k, i, 1, k],
          b_pred_ana[k, i, 2, k], b_pred_ana[k, i, 3, k],
          b_pred_ana[k, i, 4, k])
    print("ecart_pred-ana60", ecart_pred[i+I_ANA, k])


def Affiche_Reference(buffer, b_pred_ref, ecart_pred):
    """
    affichage du predicteur reference
    """
    k = AFFICHE_HORIZON
    print("pred-ref0...pred_ref3", b_pred_ref[0, 0, k], b_pred_ref[0, 1, k],
          b_pred_ref[0, 2, k], b_pred_ref[0, 3, k])
    print("ecart_pred-ref0", "ecart_pred_ref3", ecart_pred[0+I_REF, k],
          ecart_pred[3+I_REF, k])


def Affiche_Parametre(buffer, b_pred_param, ecart_pred):
    """
    affichage du predicteur parametre
    """
    k = AFFICHE_HORIZON
    print("pred-par0 pred_par1 ", b_pred_param[0, 0, k], b_pred_param[0, 1, k])
    print("ec_pred-par0 ec_pred_par1 ", ecart_pred[0+I_PARAM, k],
          ecart_pred[1+I_PARAM, k])


def Affiche_Vent(buffer, b_pred_vent, ecart_pred):
    """
    affichage du predicteur vent
    """
    k = AFFICHE_HORIZON
    print("pred-vent0 pred_vent1 ", b_pred_vent[0, 0, k], b_pred_vent[0, 1, k])
    print("ec_pred-vent0 ec_pred_vent1 ", ecart_pred[0+I_VENT, k],
          ecart_pred[1+I_VENT, k])


def Affiche_Modele(buffer, b_pred_mod, ecart_pred):
    """
    affichage du predicteur modele
    """
    k = AFFICHE_HORIZON
    print("pred-mod0 pred_mod1 ", b_pred_mod[0, 0, k], b_pred_mod[0, 1, k])
    print("ec_pred-mod0 ec_pred_mod1 ", ecart_pred[0+I_MODELE, k],
          ecart_pred[1+I_MODELE, k])


def Affiche_Algo(buffer, b_pred_algo, coef_algo, ecart_pred):
    """
    affichage du predicteur algo
    """
    k = AFFICHE_HORIZON
    print("pred-algo0 pred_algo4 ", b_pred_algo[0, 0, k], b_pred_algo[0, 1, k],
          b_pred_algo[0, 2, k], b_pred_algo[0, 3, k], b_pred_algo[0, 4, k])
    print("coef_algo0 coef_algo3 ", coef_algo[k, 0], coef_algo[k, 1],
          coef_algo[k, 2], coef_algo[k, 3])
    print("ec_pred-algo0 ec_pred_algo3 ", ecart_pred[0+I_ALGO, k],
          ecart_pred[1+I_ALGO, k], ecart_pred[2+I_ALGO, k],
          ecart_pred[3+I_ALGO, k])


def Affiche_Constante(serie):
    """
    affichage des constantes utilisees
    """
    ligne = '  '
    ligne += "FILE_BIBLIO " + FILE_BIBLIO + ";"
    ligne += "SERIE_TRAITEE " + str(serie) + ";"
    ligne += "T_BUFFER " + str(T_BUFFER) + ";"
    ligne += "PARA_SENS  " + str(PARA_SENS) + ";"
    ligne += "AFFICHE_HORIZON " + str(AFFICHE_HORIZON) + ";"
    ligne += "MODELE_SCENARIO " + str(VENT_SCENARIO) + ";"
    ligne += "MODELE_MIN " + str(VENT_MIN) + ";"
    ligne += "MODELE_PRED " + str(VENT_PRED) + ";"
    ligne += "VENT_SCENARIO " + str(VENT_SCENARIO) + ";"
    ligne += "VENT_MIN " + str(VENT_MIN) + ";"
    ligne += "VENT_MAX " + str(VENT_MAX) + ";"
    ligne += "VENT_PRED " + str(VENT_PRED) + ";"
    ligne += "VENT_PARANA " + str(VENT_PARANA) + ";"
    ligne += "REF_SCENARIO " + str(REF_SCENARIO) + ";"
    ligne += "REF_PENTE " + str(REF_PENTE) + ";"
    ligne += "ANA_PROFONDEUR " + str(ANA_PROFONDEUR) + ";"
    ligne += "BUF_SERIE " + str(BUF_SERIE) + ";"
    ligne += "BIB_SERIE " + str(BIB_SERIE) + ";"
    ligne += "ANA_SCENARIO " + str(ANA_SCENARIO) + ";"
    ligne += "PARA_PROFONDEUR " + str(PARA_PROFONDEUR) + ";"
    ligne += "PARA_HORI_POINT " + str(PARA_HORIZON_POINT) + ";"
    ligne += "HORIZON " + str(HORIZON) + ";"
    ligne += "V_PRED_MOYEN " + str(V_PRED_MOYEN) + ";"
    ligne += "V_PENAL " + str(V_PENAL) + ";"
    ligne += "V_MEMOIRE " + str(V_MEMOIRE) + ";"
    ligne += "V_ECART " + str(V_ECART) + ";"
    ligne += "V_PREDIC " + str(V_PREDIC) + ";"
    ligne += "V_PREDIC2 " + str(V_PREDIC2) + ";"
    ligne += "V_PREDIC3 " + str(V_PREDIC3) + ";"
    ligne += "V_MOYENNE " + str(V_MOYENNE) + ";"
    ligne += "ACTIVATION_REF " + str(ACTIVATION_REF) + ";"
    ligne += "ACTIVATION_ANA " + str(ACTIVATION_ANA) + ";"
    ligne += "ACTIVATION_PARAM " + str(ACTIVATION_PARAM) + ";"
    ligne += "ACTIVATION_VENT " + str(ACTIVATION_VENT) + ";"
    ligne += "ACTIVATION_MODELE " + str(ACTIVATION_MODELE) + ";"
    ligne += "ACTIVATION_MAUVAIS " + str(ACTIVATION_MAUVAIS) + ";"
    ligne += "PRED_RESULTAT " + str(PRED_RESULTAT) + ";"
    ligne += "NB_ALGO " + str(NB_ALGO) + ";"
    ligne += "OPTI_ALGO " + str(OPTI_ALGO) + ";"
    ligne += "NB_PRED_REDUIT " + str(NB_PRED_REDUIT) + ";"
    ligne += "NB_ALGO_REDUIT " + str(NB_ALGO_REDUIT) + ";"
    ligne += "MAX_VARIATION " + str(MAX_VARIATION) + ";"
    ligne += "MAX_VALEUR " + str(MAX_VALEUR) + ";"

    return ligne


def Affiche_Prediction_Complement(indice, mat_affic, tendance, ecart_tendance,
                                  ecart_moyen, ecart_moyen_f):
    """
    complement affichage des predicteurs pour AFFICHE_HORIZON (0 si H+1)
    """
    p_pred_meil = 3 + 1
    k = AFFICHE_HORIZON
    mat_affic[k, indice + 4 + k, p_pred_meil + 2] = tendance
    mat_affic[k, indice + 4 + k, p_pred_meil + 4] = ecart_tendance
    mat_affic[k, indice + 4 + k, p_pred_meil + 5] = ecart_moyen[0]
    mat_affic[k, indice + 4 + k, p_pred_meil + 6] = ecart_moyen_f[0]


def Affiche_Prediction(indice, mat_affic, mat_entete, b_pred_mod, b_pred_vent,
                       b_pred_ref, coef_pred, mem_moy_ana, b_pred_ana,
                       b_pred_param, b_pred_filt, b_pred_meil, buffer,
                       b_pred_tab, ecart_pred, b_pred_algo, coef_algo):
    """
    affichage des predicteurs
    """
    # calcul des positions de valeurs
    p_pred_meil = 3 + 1
    p_pos_mem = p_pred_meil + 7
    p_pred = p_pos_mem + ANA_SCENARIO
    p_pred_ana = p_pred + 2 * REF_SCENARIO
    p_pred_param = p_pred_ana + 2 * ANA_SCENARIO
    p_pred_vent = p_pred_param + 2 * PRED_RESULTAT
    p_pred_mod = p_pred_vent + 2 * VENT_SCENARIO
    p_pred_algo = p_pred_mod + 2 * MODELE_SCENARIO
    p_pred_tab = p_pred_algo + 3 * NB_ALGO
    mat_entete[:] = " "

    # generation de la matrice liee aux entetes des colonnes
    mat_entete[0] = " "
    mat_entete[1] = "serie"
    mat_entete[2] = "ecrete"
    mat_entete[p_pred_meil + 0] = "pred meilleur"
    mat_entete[p_pred_meil + 1] = "pred filtre"
    mat_entete[p_pred_meil + 2] = "tendance"
    mat_entete[p_pred_meil + 3] = "ecart meilleur"
    mat_entete[p_pred_meil + 4] = "ecart tendance"
    mat_entete[p_pred_meil + 5] = "ecart moyen"
    mat_entete[p_pred_meil + 6] = "ecart moy filtre"
    for i in range(ANA_SCENARIO):
        mat_entete[p_pos_mem + i] = "moy ana " + str(i)
    for i in range(REF_SCENARIO):
        mat_entete[p_pred + 2 * i] = "pred ref" + str(i)
        mat_entete[p_pred + 2 * i + 1] = "ecart ref" + str(i)
    for i in range(ANA_SCENARIO):
        mat_entete[p_pred_ana + 2 * i] = "pred ana" + str(i)
        mat_entete[p_pred_ana + 2 * i + 1] = "ecart ana" + str(i)
    for i in range(PRED_RESULTAT):
        mat_entete[p_pred_param + 2 * i] = "pred param" + str(i)
        mat_entete[p_pred_param + 2 * i + 1] = "ecart param" + str(i)
    for i in range(VENT_SCENARIO):
        mat_entete[p_pred_vent + 2 * i] = "pred vent" + str(i)
        mat_entete[p_pred_vent + 2 * i + 1] = "ecart vent" + str(i)
    for i in range(MODELE_SCENARIO):
        mat_entete[p_pred_mod + 2 * i] = "pred model" + str(i)
        mat_entete[p_pred_mod + 2 * i + 1] = "ecart model" + str(i)
    for i in range(NB_ALGO):
        mat_entete[p_pred_algo + 3 * i] = "pred algo" + str(i)
        mat_entete[p_pred_algo + 3 * i + 1] = "coeff algo" + str(i)
        mat_entete[p_pred_algo + 3 * i + 2] = "ecart algo" + str(i)
    for i in range(NB_PREDICTEURS):
        for j in range(NB_ALGO):
            mat_entete[p_pred_tab+i*NB_ALGO+j] = "coef pr" + str(i) + " al" + \
                str(j) + " "

    # generation de la matrice liee aux resultats par colonnes
    for k in range(HORIZON):
        mat_affic[k, indice + 4, 1] = buffer[NON_FILTRE, T_BUFFER]
        mat_affic[k, indice + 4, 2] = buffer[ECRETE, T_BUFFER]
        mat_affic[k, indice + 4 + k, p_pred_meil+0] = b_pred_meil[0, k]
        mat_affic[k, indice + 4 + k, p_pred_meil+1] = b_pred_filt[0, k]
        mat_affic[k, indice + 4 + k, p_pred_meil+3] = ecart_pred[I_MEILLEUR, k]
        for i in range(ANA_SCENARIO):
            mat_affic[k, indice+4+k, p_pos_mem+i] = mem_moy_ana[i]
        for i in range(REF_SCENARIO):
            mat_affic[k, indice+4+k, p_pred+2*i] = b_pred_ref[0, i, k]
            mat_affic[k, indice+4+k, p_pred+2*i+1] = ecart_pred[i+I_REF, k]
        for i in range(ANA_SCENARIO):
            j = int(round(mem_moy_ana[i], 0))
            mat_affic[k, indice+4+k, p_pred_ana+2*i] = b_pred_ana[0, i, j, k]
            mat_affic[k, indice+4+k, p_pred_ana+2*i+1] = ecart_pred[i+I_ANA, k]
        for i in range(PRED_RESULTAT):
            mat_affic[k, indice+4+k, p_pred_param+2*i] = b_pred_param[0, i, k]
            mat_affic[k, indice + 4 + k, p_pred_param + 2 * i + 1] = \
                ecart_pred[i + I_PARAM, k]
        for i in range(VENT_SCENARIO):
            mat_affic[k, indice+4+k, p_pred_vent+2*i] = b_pred_vent[0, i, k]
            mat_affic[k, indice + 4 + k, p_pred_vent + 2 * i + 1] = \
                ecart_pred[i + I_VENT, k]
        for i in range(MODELE_SCENARIO):
            mat_affic[k, indice+4+k, p_pred_mod+2*i] = b_pred_mod[0, i, k]
            mat_affic[k, indice + 4 + k, p_pred_mod + 2 * i + 1] = \
                ecart_pred[i + I_MODELE, k]
        for i in range(NB_ALGO):
            mat_affic[k, indice+4+k, p_pred_algo+3*i] = b_pred_algo[0, i, k]
            mat_affic[k, indice + 4 + k, p_pred_algo+3*i+1] = coef_algo[k, i]
            mat_affic[k, indice+4+k, p_pred_algo+3*i+2] = \
                ecart_pred[i+I_ALGO, k]
        for i in range(NB_PREDICTEURS):
                for j in range(NB_ALGO):
                    mat_affic[k, indice+4+k, p_pred_tab+i*NB_ALGO+j] =\
                        coef_pred[k, i, j]
