# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:03:47 2016

@author: Philippe

essai d appel de la prediction
"""

from numpy import zeros, loadtxt
import predicteur as pred
from constante import ANNEE_POINT, HEURE_POINT, HORIZON, V_MODELE, V_VENT, \
    JOUR_POINT, MOIS_POINT, NON_FILTRE, VAL_ANNEE, VAL_HEURE, VAL_JOUR, \
    VAL_MOIS, VAL_VALEUR, N_ATTRIBUT
from constante_instal import N2AIXA, N2AIXC, N2CINQ, N2PLOM, O3AIXA, O3AIXP, \
    O3CINQ, PCAIXA, PCAIXC, PCCINQ, PCRABA, PCSTLO, N2RABA, N2STLO, AIXVV, \
    PCCINQ_MORGAN, VV1_MORGAN, VV2_MORGAN


def Lecture_Nouvelle_Valeur(instant, donnees):
    """ simulation d'acquisition de nouvelles mesures :
        Instant : numéro horaire de la données à partir du 1/1/2014 0h
        données : liste des mesures initialisées"""
    valeur = zeros((5))
    valeur[VAL_VALEUR] = donnees[NON_FILTRE, instant]
    valeur[VAL_HEURE] = donnees[HEURE_POINT, instant]
    valeur[VAL_JOUR] = donnees[JOUR_POINT, instant]
    valeur[VAL_MOIS] = donnees[MOIS_POINT, instant]
    valeur[VAL_ANNEE] = donnees[ANNEE_POINT, instant]
    return valeur


def Lecture_Nouvelle_Valeur_Vent(instant, donnees):
    """ simulation d'acquisition de nouvelles vitesse vent :
        Instant : numéro horaire de la données à partir du 1/1/2014 0h
        données : liste des mesures initialisées"""
    v_vent = zeros((HORIZON + 1))
    for i in range(HORIZON + 1):
        v_vent[i] = donnees[V_VENT, instant + i + 1]
    return v_vent


def Lecture_Nouvelle_Valeur_Modele(instant, donnees):
    """ simulation d'acquisition de nouvelles previsions de modelisation :
        Instant : numéro horaire de la données à partir du 1/1/2014 0h
        données : liste des mesures initialisées"""
    donnees_modele = zeros((HORIZON + 1))
    for i in range(HORIZON + 1):
        donnees_modele[i] = donnees[V_MODELE, instant + i + 1]
    return donnees_modele


def Valeurs_Morgan():
    """
    chargement et initialisation des mesures
    fichier bibliotheque : 13866 lignes
    fichier mesure : 3672 lignes
    annee, mois, jour, heure : colonne 0 à 3
    mesure : colonne 4
    valeur du vent : colonne 5 ou 6
    valeur du mod_air : colonne 7
    """
    fichier_mesure = """./mesures_Morgan2.csv"""
    mesure_brut = loadtxt(fichier_mesure, delimiter=';', skiprows=1)
    serie_vent = 6
    N_LIGNE_MESURE = 3672
    mesure = zeros((N_ATTRIBUT+1, N_LIGNE_MESURE+1))
    for i in range(1, N_LIGNE_MESURE):
        mesure[ANNEE_POINT, i] = mesure_brut[i - 1, 0]
        mesure[MOIS_POINT, i] = mesure_brut[i - 1, 1]
        mesure[JOUR_POINT, i] = mesure_brut[i - 1, 2]
        mesure[HEURE_POINT, i] = mesure_brut[i - 1, 3]
        mesure[NON_FILTRE, i] = mesure_brut[i - 1, 4]
        mesure[V_VENT, i] = mesure_brut[i - 1, serie_vent]
        mesure[V_MODELE, i] = mesure_brut[i - 1, 7]
    return mesure


def Essai_Predicteur1():
    """ essai avec réinitialisation de la classe a chaque pas de temps"""
    N_RESULT = 3600    # nombre de donnees traitees (9000), 90, 900, 3600
    N_DEPART = 26    # premiere ligne des donnees traitees, 26
    reset_prediction = True
    resultat = zeros((HORIZON))
    # serie_traitee = N2AIXA
    # serie_vent = AIXVV
    serie_traitee = PCCINQ_MORGAN
    serie_vent = VV2_MORGAN
    for instant in range(N_DEPART, N_RESULT + 1):
        pred1 = pred.predicteur(serie_traitee, reset_prediction, serie_vent)
        # pred1 = pred.predicteur(serie_traitee, reset_prediction)
        # mesure = pred1.donnees
        mesure = Valeurs_Morgan()
        nouv_valeur = Lecture_Nouvelle_Valeur(instant-1, mesure)
        v_vent = Lecture_Nouvelle_Valeur_Vent(instant-1, mesure)
        mod_air = Lecture_Nouvelle_Valeur_Modele(instant-1, mesure)
        print("valeur : ", nouv_valeur[0], " prévu : ", resultat[0],
              " écart : ", (nouv_valeur[0] - resultat[0]))
        resultat = pred1.Prediction(nouv_valeur)
        # resultat = pred1.Prediction(nouv_valeur, vitesse_vent=v_vent)
        # resultat =  pred1.Prediction(nouv_valeur, modele=mod_air)
        # resultat = pred1.Prediction(nouv_valeur, v_vent, mod_air)
        # print("resultat", resultat)
        del pred1
        reset_prediction = False


def Essai_Predicteur2():
    """ essai sans reinitialisation de la classe """
    N_RESULT = 89    # nombre de donnees traitees (9000), 90, 900, 3600
    N_DEPART = 1    # premiere ligne des donnees traitees, 26
    reset_prediction = True
    resultat = zeros((HORIZON))
    resultat_filtre = zeros((HORIZON))
    serie_traitee = N2CINQ
    # serie_vent = AIXVV
    # serie_traitee = PCCINQ_MORGAN
    # serie_vent = VV2_MORGAN
    pred1 = pred.predicteur(serie_traitee, reset_prediction)
    # pred1 = pred.predicteur(serie_traitee, reset_prediction, serie_vent)
    # mesure = pred1.donnees
    mesure = Valeurs_Morgan()
    for instant in range(N_DEPART, N_RESULT + 1):
        nouv_valeur = Lecture_Nouvelle_Valeur(instant-1, mesure)
        v_vent = Lecture_Nouvelle_Valeur_Vent(instant-1, mesure)
        mod_air = Lecture_Nouvelle_Valeur_Modele(instant-1, mesure)
        resultat = pred1.Prediction(nouv_valeur)
        # resultat = pred1.Prediction(nouv_valeur, vitesse_vent=v_vent)
        # resultat = pred1.Prediction(nouv_valeur, modele=mod_air)
        # resultat = pred1.Prediction(nouv_valeur, v_vent, mod_air)
        print("valeur : ", nouv_valeur[0], pred1.Info_Date(), " prévu : ", resultat)
        date_mesure = pred1.Info_Date()
        tendance = pred1.Tendance()
        ecart_moyen = pred1.Ecart_Moyen(1)
        ecart_moyen_f = pred1.Ecart_Moyen_Filtre(1)
        ecart_tendance = pred1.Ecart_Tendance()
        # resultat_filtre = pred1.Prediction_Filtre(nouv_valeur, v_vent)
        # print("resultat1", resultat)
        if instant % 100 == 0:
            print("instant : ", instant)
        # if instant == N_RESULT:
        #     pred1.Debug_Pred()
    del pred1

Essai_Predicteur2()
