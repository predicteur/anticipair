# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 13:19:04 2016

@author: Philippe

Affichage des valeurs intermédiaires pour debug
"""

from constante import ANA_SCENARIO, DEBUG_PREDICTION1, FILTRE, HEURE_POINT, \
    HORIZON, NB_PREDICTEURS, NON_FILTRE, N_LIGNE, PRED_RESULTAT, SEQUENCE, \
    TAILLE_BUFFER, TYPE_POINT, VENT_SCENARIO, NB_ALGO, REF_SCENARIO, \
    I_ANA, I_PARAM, I_MEILLEUR, I_REF, I_VENT, I_ALGO, N_RESULT, \
    N_DEPART, AFFICHE_HORIZON, V_PREDIC, V_PREDIC2, V_PREDIC3, V_MOYENNE, \
    ANA_PROFONDEUR, ANA_FILTRAGE, ANA_FILTRAGE_BIBLIO, PARA_PROFONDEUR, \
    PARA_HORIZON_POINT, FILE_BIBLIO, PARA_SENS, VENT_MIN, VENT_MAX, VENT_PRED,\
    VENT_PARANA, REF_PENTE, V_PRED_MOYEN, V_PENAL, V_MEMOIRE, V_ECART, \
    ACTIVATION_REF, ACTIVATION_ANA, ACTIVATION_PARAM, ACTIVATION_VENT, \
    ACTIVATION_MAUVAIS, OPTI_ALGO


def Affiche_Donnees_Traitees(donnees):
    """
    affichage de la bibliotheque
    """
    print("heure", "non-filtre", "sequence", "type_point", "filtre")
    # for i in range(1, 10):
    for i in range(6184, 6204):
        print(donnees[HEURE_POINT, i],
              donnees[NON_FILTRE, i],
              donnees[SEQUENCE, i],
              donnees[TYPE_POINT, i],
              donnees[FILTRE, i])
    print(donnees[HEURE_POINT, N_LIGNE - 1],
          donnees[NON_FILTRE, N_LIGNE - 1],
          donnees[SEQUENCE, N_LIGNE - 1],
          donnees[TYPE_POINT, N_LIGNE - 1],
          donnees[FILTRE, N_LIGNE - 1])


def Affiche_Buffer(buffer):
    """
    affichage du buffer
    """
    print("non filtre", "filtre", "sequence", "type_point", "heure", "jour",
          "mois", "annee")
    print(buffer)


def Affiche_Analogie(buffer, b_pred_analogie, ecart_predicteur):
    """
    affichage du predicteur analogie
    """
    i = 6
    k = 0
    print("b_pred-ana0600", "b_pred_ana0640",
          b_pred_analogie[k, i, 0, k], b_pred_analogie[k, i, 1, k],
          b_pred_analogie[k, i, 2, k], b_pred_analogie[k, i, 3, k],
          b_pred_analogie[k, i, 4, k])
    print("ecart_pred-ana60", ecart_predicteur[i+I_ANA, k])


def Affiche_Reference(buffer, b_pred_reference, ecart_predicteur):
    """
    affichage du predicteur reference
    """
    k = 0
    print("pred-ref0...pred_ref3", b_pred_reference[0, 0, k],
          b_pred_reference[0, 1, k], b_pred_reference[0, 2, k],
          b_pred_reference[0, 3, k])
    print("ecart_pred-ref0", "ecart_pred_ref3", ecart_predicteur[0+I_REF, k],
          ecart_predicteur[3+I_REF, k])


def Affiche_Parametre(buffer, b_pred_parametre, ecart_predicteur):
    """
    affichage du predicteur parametre
    """
    k = 0
    print("pred-para0", "pred_para1", b_pred_parametre[0, 0, k],
          b_pred_parametre[0, 1, k])
    print("ecart_pred-para0", "ecart_pred_para1",
          ecart_predicteur[0+I_PARAM, k], ecart_predicteur[1+I_PARAM, k])


def Affiche_Vent(buffer, b_pred_vent, ecart_predicteur):
    """
    affichage du predicteur vent
    """
    k = 0
    print("pred-vent0", "pred_vent1",
          b_pred_vent[0, 0, k], b_pred_vent[0, 1, k])
    print("ecart_pred-vent0", "ecart_pred_vent1",
          ecart_predicteur[0+I_VENT, k], ecart_predicteur[1+I_VENT, k])


def Affiche_Algo(buffer, b_pred_algo, coef_algo, ecart_predicteur):
    """
    affichage du predicteur algo
    """
    k = 0
    print("pred-algo0", "pred_algo4",
          b_pred_algo[0, 0, k], b_pred_algo[0, 1, k], b_pred_algo[0, 2, k],
          b_pred_algo[0, 3, k], b_pred_algo[0, 4, k])
    print("coef_algo0", "coef_algo3",
          coef_algo[k, 0], coef_algo[k, 1], coef_algo[k, 2], coef_algo[k, 3])
    print("ecart_pred-algo0", "ecart_pred_algo3",
          ecart_predicteur[0+I_ALGO, k], ecart_predicteur[1+I_ALGO, k],
          ecart_predicteur[2+I_ALGO, k], ecart_predicteur[3+I_ALGO, k])


def Affiche_Constante(serie):
    """
    affichage des constantes utilisees
    """
    ligne = '  '
    ligne += "FILE_BIBLIO " + FILE_BIBLIO + ";"
    ligne += "SERIE_TRAITEE " + str(serie) + ";"
    ligne += "N_RESULT " + str(N_RESULT) + ";"
    ligne += "N_DEPART " + str(N_DEPART) + ";"
    ligne += "TAILLE_BUFFER " + str(TAILLE_BUFFER) + ";"
    ligne += "PARA_SENS  " + str(PARA_SENS) + ";"
    ligne + "AFFICHE_HORIZON " + str(AFFICHE_HORIZON) + ";"
    ligne += "VENT_SCENARIO " + str(VENT_SCENARIO) + ";"
    ligne += "VENT_MIN " + str(VENT_MIN) + ";"
    ligne += "VENT_MAX " + str(VENT_MAX) + ";"
    ligne += "VENT_PRED " + str(VENT_PRED) + ";"
    ligne += "VENT_PARANA " + str(VENT_PARANA) + ";"
    ligne += "REF_SCENARIO " + str(REF_SCENARIO) + ";"
    ligne += "REF_PENTE " + str(REF_PENTE) + ";"
    ligne += "ANA_PROFONDEUR " + str(ANA_PROFONDEUR) + ";"
    ligne += "ANA_FILTRAGE " + str(ANA_FILTRAGE) + ";"
    ligne += "ANA_FILT_BIBLI " + str(ANA_FILTRAGE_BIBLIO) + ";"
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
    ligne += "ACTIVATION_MAUVAIS " + str(ACTIVATION_MAUVAIS) + ";"
    ligne += "PRED_RESULTAT " + str(PRED_RESULTAT) + ";"
    ligne += "NB_ALGO " + str(NB_ALGO) + ";"
    ligne += "OPTI_ALGO " + str(OPTI_ALGO) + ";"

    return ligne


def Affiche_Prediction_Complement(indice, mat_affic, tendance, ecart_tendance,
                                  ecart_moyen, ecart_moyen_f):
    """
    complement affichage des predicteurs pour H+1
    """
    p_pred_meilleur = 3 + 1
    k = 0
    mat_affic[k, indice + 4 + k, p_pred_meilleur + 2] = tendance
    mat_affic[k, indice + 4 + k, p_pred_meilleur + 4] = ecart_tendance
    mat_affic[k, indice + 4 + k, p_pred_meilleur + 5] = ecart_moyen[0]
    mat_affic[k, indice + 4 + k, p_pred_meilleur + 6] = ecart_moyen_f[0]


def Affiche_Prediction(indice, mat_affic, mat_entete, b_pred_vent,
                       b_pred_reference, coef_predicteur, memoire_moyenne_ana,
                       b_pred_analogie,
                       b_pred_parametre, b_pred_filtre, b_pred_meilleur,
                       buffer, b_pred_tableau, ecart_predicteur, b_pred_algo,
                       coef_algo):
    """
    affichage des predicteurs
    """
    # calcul des positions de valeurs
    p_pred_meilleur = 3 + 1
    pos_memoire = p_pred_meilleur + 7
    p_pred = pos_memoire + ANA_SCENARIO
    p_pred_ana = p_pred + 2 * REF_SCENARIO
    p_pred_param = p_pred_ana + 2 * ANA_SCENARIO
    p_pred_vent = p_pred_param + 2 * PRED_RESULTAT
    p_pred_algo = p_pred_vent + 2 * VENT_SCENARIO
    p_pred_tableau = p_pred_algo + 3 * NB_ALGO
    mat_entete[:] = " "

    # generation de la matrice liee aux entetes des colonnes
    mat_entete[0] = " "
    mat_entete[1] = "serie"
    mat_entete[2] = "filtre"
    mat_entete[p_pred_meilleur + 0] = "pred meilleur"
    mat_entete[p_pred_meilleur + 1] = "pred filtre"
    mat_entete[p_pred_meilleur + 2] = "tendance"
    mat_entete[p_pred_meilleur + 3] = "ecart meilleur"
    mat_entete[p_pred_meilleur + 4] = "ecart tendance"
    mat_entete[p_pred_meilleur + 5] = "ecart moyen"
    mat_entete[p_pred_meilleur + 6] = "ecart moy filtre"
    for i in range(ANA_SCENARIO):
        mat_entete[pos_memoire + i] = "moy ana " + str(i)
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
    for i in range(NB_ALGO):
        mat_entete[p_pred_algo + 3 * i] = "pred algo" + str(i)
        mat_entete[p_pred_algo + 3 * i + 1] = "coeff algo" + str(i)
        mat_entete[p_pred_algo + 3 * i + 2] = "ecart algo" + str(i)
    for i in range(NB_PREDICTEURS):
        for j in range(NB_ALGO):
            mat_entete[p_pred_tableau+i*NB_ALGO+j] = "coef pr" + str(i)\
                + " al" + str(j) + " "

    # generation de la matrice liee aux resultats par colonnes
    for k in range(HORIZON):
        mat_affic[k, indice + 4, 1] = buffer[NON_FILTRE, TAILLE_BUFFER]
        mat_affic[k, indice + 4, 2] = buffer[FILTRE, TAILLE_BUFFER]
        mat_affic[k, indice + 4 + k, p_pred_meilleur+0] = b_pred_meilleur[0, k]
        mat_affic[k, indice + 4 + k, p_pred_meilleur + 1] = b_pred_filtre[0, k]
        mat_affic[k, indice + 4 + k, p_pred_meilleur + 3] = \
            ecart_predicteur[I_MEILLEUR, k]
        for i in range(ANA_SCENARIO):
            mat_affic[k, indice+4+k, pos_memoire+i] = memoire_moyenne_ana[i]
        for i in range(REF_SCENARIO):
            mat_affic[k, indice+4+k, p_pred+2*i] = b_pred_reference[0, i, k]
            mat_affic[k, indice+4+k, p_pred+2*i+1] = \
                ecart_predicteur[i+I_REF, k]
            # mat_affic[k, indice+4+k, p_pred+2*i+1] = coef_predicteur[k, i, 1]
        for i in range(ANA_SCENARIO):
            j = round(memoire_moyenne_ana[i], 0)
            mat_affic[k, indice+4+k, p_pred_ana+2*i] = \
                b_pred_analogie[0, i, j, k]
            # mat_affic[k, indice + 4 + k, p_pred_ana + 2 * i + 1] = \
            #     coef_predicteur[k, i + I_ANA, 1]
            mat_affic[k, indice + 4 + k, p_pred_ana + 2 * i + 1] = \
                ecart_predicteur[i + I_ANA, k]
        for i in range(PRED_RESULTAT):
            mat_affic[k, indice + 4 + k, p_pred_param + 2 * i] = \
                b_pred_parametre[0, i, k]
            # mat_affic[k, indice + 4 + k, p_pred_param + 2 * i + 1] = \
            #    coef_predicteur[k, i + I_PARAM, 1]
            mat_affic[k, indice + 4 + k, p_pred_param + 2 * i + 1] = \
                ecart_predicteur[i + I_PARAM, k]
        for i in range(VENT_SCENARIO):
            mat_affic[k, indice+4+k, p_pred_vent+2*i] = b_pred_vent[0, i, k]
            # mat_affic[k, indice + 4 + k, p_pred_vent + 2 * i + 1] = \
            #    coef_predicteur[k, i + I_VENT, 1]
            mat_affic[k, indice + 4 + k, p_pred_vent + 2 * i + 1] = \
                ecart_predicteur[i + I_VENT, k]
        for i in range(NB_ALGO):
            mat_affic[k, indice+4+k, p_pred_algo+3*i] = b_pred_algo[0, i, k]
            mat_affic[k, indice + 4 + k, p_pred_algo+3*i+1] = coef_algo[k, i]
            mat_affic[k, indice+4+k, p_pred_algo+3*i+2] = \
                ecart_predicteur[i + I_ALGO, k]
        for i in range(NB_PREDICTEURS):
                for j in range(NB_ALGO):
                    mat_affic[k, indice+4+k, p_pred_tableau+i*NB_ALGO+j] =\
                        coef_predicteur[k, i, j]

    # affichage des resultats en ligne
    if DEBUG_PREDICTION1:
        k = 0
        print("non filtre", "filtre", "b_pred_meil", "ecart_pred_meil**2")
        print(buffer[NON_FILTRE, TAILLE_BUFFER], buffer[FILTRE, TAILLE_BUFFER],
              b_pred_meilleur[0, k], ecart_predicteur[I_MEILLEUR, k]**2)
        print("mem_ana(0) ... mem_ana(7)")
        print(memoire_moyenne_ana[0], memoire_moyenne_ana[1],
              memoire_moyenne_ana[2], memoire_moyenne_ana[3],
              memoire_moyenne_ana[4], memoire_moyenne_ana[5],
              memoire_moyenne_ana[6], memoire_moyenne_ana[7])
        print("pred-ref0", "pred_ref1", "pred_ref2")
        print(b_pred_reference[0, 0, k], b_pred_reference[0, 1, k],
              b_pred_reference[0, 2, k])
        print("coef_pred-ref0, coef_pred_ref1, coef_pred_ref2")
        print(coef_predicteur[k, 0+I_REF, 1], coef_predicteur[k, 1+I_REF, 1],
              coef_predicteur[k, 2+I_REF, 1])
        j0 = round(memoire_moyenne_ana[0], 0)
        j1 = round(memoire_moyenne_ana[1], 0)
        j2 = round(memoire_moyenne_ana[2], 0)
        j3 = round(memoire_moyenne_ana[3], 0)
        j4 = round(memoire_moyenne_ana[4], 0)
        j5 = round(memoire_moyenne_ana[5], 0)
        j6 = round(memoire_moyenne_ana[6], 0)
        j7 = round(memoire_moyenne_ana[7], 0)
        print("pred-ana0, pred_ana1, pred_ana2, ....  pred_ana7")
        print(b_pred_analogie[0, 0, j0, k],
              b_pred_analogie[0, 1, j1, k],
              b_pred_analogie[0, 2, j2, k],
              b_pred_analogie[0, 3, j3, k],
              b_pred_analogie[0, 4, j4, k],
              b_pred_analogie[0, 5, j5, k],
              b_pred_analogie[0, 6, j6, k],
              b_pred_analogie[0, 7, j7, k])
        print("coef_pred-ana0, ana1, ana2, ... , ana7")
        print(coef_predicteur[k, 0 + I_ANA, 1],
              coef_predicteur[k, 1 + I_ANA, 1],
              coef_predicteur[k, 2 + I_ANA, 1],
              coef_predicteur[k, 3 + I_ANA, 1],
              coef_predicteur[k, 4 + I_ANA, 1],
              coef_predicteur[k, 5 + I_ANA, 1],
              coef_predicteur[k, 6 + I_ANA, 1],
              coef_predicteur[k, 7 + I_ANA, 1])
        print("pred-para0, pred_para1, pred_para2, pred_para3, pred_para4")
        print(b_pred_parametre[0, 0, k],
              b_pred_parametre[0, 1, k],
              b_pred_parametre[0, 2, k],
              b_pred_parametre[0, 3, k],
              b_pred_parametre[0, 4, k])
        print("coef_pred-para0, para1, para2, para3, para4")
        print(coef_predicteur[k, 0 + I_PARAM, 1],
              coef_predicteur[k, 1 + I_PARAM, 1],
              coef_predicteur[k, 2 + I_PARAM, 1],
              coef_predicteur[k, 3 + I_PARAM, 1],
              coef_predicteur[k, 4 + I_PARAM, 1])
        print("pred-vent0, pred_vent1, pred_vent2, pred_vent3, pred_vent4")
        print(b_pred_vent[0, 0, k],
              b_pred_vent[0, 1, k],
              b_pred_vent[0, 2, k],
              b_pred_vent[0, 3, k],
              b_pred_vent[0, 4, k])
        print("coef_pred-vent0, vent1, vent2, vent3, vent4")
        print(coef_predicteur[k, 0 + I_VENT, 1],
              coef_predicteur[k, 1 + I_VENT, 1],
              coef_predicteur[k, 2 + I_VENT, 1],
              coef_predicteur[k, 3 + I_VENT, 1],
              coef_predicteur[k, 4 + I_VENT, 1])
        print("pred-algo0, pred_algo1, pred_algo2, pred_algo3, pred_algo4")
        print(b_pred_algo[0, 0, k],
              b_pred_algo[0, 1, k],
              b_pred_algo[0, 2, k],
              b_pred_algo[0, 3, k],
              b_pred_algo[0, 4, k])
        print("coef_pred-algo0, algo1, algo2, algo3, algo4")
        print(coef_algo[k, 0],
              coef_algo[k, 1],
              coef_algo[k, 2],
              coef_algo[k, 3],
              coef_algo[k, 4])
