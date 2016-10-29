# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 13:19:04 2016

@author: Philippe

Affichage des valeurs intermédiaires pour debug
"""

from constante import ACTIVATION_ANA, ACTIVATION_PARAM, ACTIVATION_REF,\
    AFFICHE_HORIZON, ANA_ECART_MC, ANA_FILTRAGE, ANA_FILTRAGE_BIBLIO, \
    ANA_HEURE, ANA_PROFONDEUR, ANA_SCENARIO, ANNEE_POINT, C_MEM_ANA, \
    C_MEM_PARAM, DATE_INIT, DEBUG_ANALOGIE, DEBUG_BUFFER, DEBUG_DONNEES, \
    DEBUG_PARAMETRE, DEBUG_PREDICTION, DEBUG_PREDICTION1, DEBUG_PREDICTION2, \
    DEBUG_PREDICTION3, DEBUG_PREDICTION4, DEBUG_PREDICTION5, DEB_MATIN, \
    DEB_MIDI, DEB_NUIT, DEB_SOIR, FILE_BIBLIO, FILTRE, HEURE_POINT, HORIZON, \
    INTER_POINT, JOUR_POINT, MATIN, MAXI, MAX_POINT, MAX_SEQ, \
    MIDI, MIN_POINT, MIN_SEQ, MOIS_POINT, N2AIXA, N2AIXC, N2CINQ, N2PLOM, \
    N2RABA, N2STLO, NB_PREDICTEURS, NB_SEQ, NON_FILTRE, NUIT, N_ATTRIBUT,\
    N_DEPART, N_LIGNE, N_RESULT, O3AIXA, O3AIXP, O3CINQ, PARA_ECART_MC, \
    PARA_HEURE, PARA_HORIZON_POINT, PARA_PROFONDEUR, PARA_SENS, PCAIXA, \
    PCAIXC, PCCINQ, PCRABA, PCSTLO, PRED_RESULTAT, SEQUENCE, \
    SOIR, TAILLE_BUFFER, TIME_HEURE, TYPE_POINT, VAL_ANNEE, VAL_HEURE, \
    VAL_JOUR, VAL_MOIS, VAL_VALEUR, V_MOYENNE, V_PREDIC, V_PREDIC2, V_PREDIC3,\
    REF_SCENARIO


def Affiche_Donnees_Traitees(donnees):

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

    print("non filtre", "filtre", "sequence", "type_point", "heure", "jour",
          "mois", "annee")
    print(buffer)


def Affiche_Analogie(buffer, b_prediction_analogie,
                     ecart_pred_analogie, resultat_analogie,
                     ecart_analogie_global):

    i = 6
    k = 0
    print("b_pred-ana0600", "b_pred_ana0640")
    print(b_prediction_analogie[k, i, 0, k],
          b_prediction_analogie[k, i, 1, k],
          b_prediction_analogie[k, i, 2, k],
          b_prediction_analogie[k, i, 3, k],
          b_prediction_analogie[k, i, 4, k])
    print("ecart_pred-ana600", "ecart_pred_ana640")
    print(ecart_pred_analogie[i, 0, k],
          ecart_pred_analogie[i, 1, k],
          ecart_pred_analogie[i, 2, k],
          ecart_pred_analogie[i, 3, k],
          ecart_pred_analogie[i, 4, k])
    print("ecart_ana_global60", "ecart_ana_global64")
    print(ecart_analogie_global[i, 0],
          ecart_analogie_global[i, 1],
          ecart_analogie_global[i, 2],
          ecart_analogie_global[i, 3],
          ecart_analogie_global[i, 4])
    print("resultat-ana0 ... resultat-ana5 ")
    print(resultat_analogie[ANA_HEURE, 0], resultat_analogie[ANA_HEURE, 1],
          resultat_analogie[ANA_HEURE, 2], resultat_analogie[ANA_HEURE, 3],
          resultat_analogie[ANA_HEURE, 4], resultat_analogie[ANA_HEURE, 5])
    print("ecartmc-ana0 ... ecartmc-ana5 ")
    print(resultat_analogie[ANA_ECART_MC, 0],
          resultat_analogie[ANA_ECART_MC, 1],
          resultat_analogie[ANA_ECART_MC, 2],
          resultat_analogie[ANA_ECART_MC, 3],
          resultat_analogie[ANA_ECART_MC, 4],
          resultat_analogie[ANA_ECART_MC, 5])


def Affiche_Parametre(buffer, b_prediction_parametre,
                      ecart_pred_parametre, resultat_parametre):

    k = 0
    print("pred-para0", "pred_para1")
    print(b_prediction_parametre[0, 0, k],
          b_prediction_parametre[0, 1, k])
    print("ecart_pred-para0", "ecart_pred_para1")
    print(ecart_pred_parametre[0, k],
          ecart_pred_parametre[1, k])
    print("resultat-para0 a resultat-para4 ")
    print(resultat_parametre[PARA_HEURE, 0], resultat_parametre[PARA_HEURE, 1],
          resultat_parametre[PARA_HEURE, 2], resultat_parametre[PARA_HEURE, 3],
          resultat_parametre[PARA_HEURE, 4])


def Affiche_Prediction(b_prediction_reference, coef_predicteur,
                       memoire_moyenne_ana, b_prediction_analogie,
                       b_prediction_parametre, b_prediction_meilleur,
                       ecart_pred_meilleur, buffer):

    if DEBUG_PREDICTION1:
        k = 0
        print("non filtre", "filtre", "b_pred_meil", "ecart_pred_meil")
        print(buffer[NON_FILTRE, TAILLE_BUFFER], buffer[FILTRE, TAILLE_BUFFER],
              b_prediction_meilleur[0, k], ecart_pred_meilleur[k]**2)
        print("mem_ana(0) ... mem_ana(7)")
        print(memoire_moyenne_ana[0], memoire_moyenne_ana[1],
              memoire_moyenne_ana[2], memoire_moyenne_ana[3],
              memoire_moyenne_ana[4], memoire_moyenne_ana[5],
              memoire_moyenne_ana[6], memoire_moyenne_ana[7])
        print("pred-ref0", "pred_ref1", "pred_ref2")
        print(b_prediction_reference[0, 0, k], b_prediction_reference[0, 1, k],
              b_prediction_reference[0, 2, k])
        print("coef_pred-ref0, coef_pred_ref1, coef_pred_ref2")
        print(coef_predicteur[k, 0], coef_predicteur[k, 1],
              coef_predicteur[k, 2])
        j0 = round(memoire_moyenne_ana[0], 0)
        j1 = round(memoire_moyenne_ana[1], 0)
        j2 = round(memoire_moyenne_ana[2], 0)
        j3 = round(memoire_moyenne_ana[3], 0)
        j4 = round(memoire_moyenne_ana[4], 0)
        j5 = round(memoire_moyenne_ana[5], 0)
        j6 = round(memoire_moyenne_ana[6], 0)
        j7 = round(memoire_moyenne_ana[7], 0)
        print("pred-ana0, pred_ana1, pred_ana2, ....  pred_ana7")
        print(b_prediction_analogie[0, 0, j0, k],
              b_prediction_analogie[0, 1, j1, k],
              b_prediction_analogie[0, 2, j2, k],
              b_prediction_analogie[0, 3, j3, k],
              b_prediction_analogie[0, 4, j4, k],
              b_prediction_analogie[0, 5, j5, k],
              b_prediction_analogie[0, 6, j6, k],
              b_prediction_analogie[0, 7, j7, k])
        print("coef_pred-ana0, ana1, ana2, ... , ana7")
        print(coef_predicteur[k, 0 + REF_SCENARIO],
              coef_predicteur[k, 1 + REF_SCENARIO],
              coef_predicteur[k, 2 + REF_SCENARIO],
              coef_predicteur[k, 3 + REF_SCENARIO],
              coef_predicteur[k, 4 + REF_SCENARIO],
              coef_predicteur[k, 5 + REF_SCENARIO],
              coef_predicteur[k, 6 + REF_SCENARIO],
              coef_predicteur[k, 7 + REF_SCENARIO])
        print("pred-para0, pred_para1, pred_para2, pred_para3, pred_para4")
        print(b_prediction_parametre[0, 0, k],
              b_prediction_parametre[0, 1, k],
              b_prediction_parametre[0, 2, k],
              b_prediction_parametre[0, 3, k],
              b_prediction_parametre[0, 4, k])
        print("coef_pred-para0, para1, para2, para3, para4")
        print(coef_predicteur[k, 0 + REF_SCENARIO + ANA_SCENARIO],
              coef_predicteur[k, 1 + REF_SCENARIO + ANA_SCENARIO],
              coef_predicteur[k, 2 + REF_SCENARIO + ANA_SCENARIO],
              coef_predicteur[k, 3 + REF_SCENARIO + ANA_SCENARIO],
              coef_predicteur[k, 4 + REF_SCENARIO + ANA_SCENARIO])
