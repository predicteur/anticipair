# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:03:47 2016

@author: Philippe

essai d appel de la prediction
"""

from numpy import zeros, loadtxt
import predicteur as pred
from constante import ANNEE_POINT, HEURE_POINT, HORIZON, \
    JOUR_POINT, MOIS_POINT, NON_FILTRE, N_DEPART, N_RESULT, \
    VAL_ANNEE, VAL_HEURE, VAL_JOUR, VAL_MOIS, VAL_VALEUR, V_VENT

from constante import N2AIXA, N2AIXC, N2CINQ, N2PLOM, O3AIXA, O3AIXP, O3CINQ, \
    PCAIXA, PCAIXC, PCCINQ, PCRABA, PCSTLO, N2RABA, N2STLO, AIXVV, \
    FILE_BIBLIO, N_ATTRIBUT, PCCINQ_MORGAN, VV1_MORGAN, VV2_MORGAN


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
    vitesse_vent = zeros((HORIZON + 1))
    for i in range(HORIZON + 1):
        vitesse_vent[i] = donnees[V_VENT, instant + i + 1]

    return vitesse_vent


def Valeurs_Morgan():
    """
    chargement et initialisation des mesures
    fichier bibliotheque : 13866 lignes
    fichier mesure : 3672 lignes
    valeur du vent : colonne 5 ou 6
    """
    fichier_mesure = """./mesures_Morgan.csv"""
    mesure = loadtxt(fichier_mesure, delimiter=';', skiprows=1)
    serie_vent = 6
    N_LIGNE_MESURE = 3672
    donnees = zeros((N_ATTRIBUT+1, N_LIGNE_MESURE+1))
    for i in range(1, N_LIGNE_MESURE):
        donnees[ANNEE_POINT, i] = mesure[i - 1, 0]
        donnees[MOIS_POINT, i] = mesure[i - 1, 1]
        donnees[JOUR_POINT, i] = mesure[i - 1, 2]
        donnees[HEURE_POINT, i] = mesure[i - 1, 3]
        donnees[NON_FILTRE, i] = mesure[i - 1, 4]
        donnees[V_VENT, i] = mesure[i - 1, serie_vent]

    return donnees


def Essai_Predicteur1():
    """ essai avec réinitialisation de la classe a chaque pas de temps"""
    reset_prediction = True
    resultat = zeros((HORIZON))
    # serie_traitee = N2AIXA
    # serie_vent = AIXVV
    serie_traitee = PCCINQ_MORGAN
    serie_vent = VV2_MORGAN
    for instant in range(N_DEPART, N_RESULT + 1):
        pred1 = pred.predicteur(serie_traitee, serie_vent, reset_prediction)
        # mesure = pred1.donnees
        mesure = Valeurs_Morgan()
        nouv_valeur = Lecture_Nouvelle_Valeur(instant-1, mesure)
        vitesse_vent = Lecture_Nouvelle_Valeur_Vent(instant-1, mesure)
        print("valeur : ", nouv_valeur[0], " prévu : ", resultat[0],
              " écart : ", (nouv_valeur[0] - resultat[0]))
        # resultat = pred1.Prediction(nouv_valeur)
        resultat = pred1.Prediction(nouv_valeur, vitesse_vent)
        # print("resultat", resultat)
        del pred1
        reset_prediction = False


def Essai_Predicteur2():
    """ essai sans reinitialisation de la classe """
    reset_prediction = True
    resultat = zeros((HORIZON))
    resultat_filtre = zeros((HORIZON))
    # serie_traitee = N2AIXA
    # serie_vent = AIXVV
    serie_traitee = PCCINQ_MORGAN
    serie_vent = VV2_MORGAN
    pred1 = pred.predicteur(serie_traitee, serie_vent, reset_prediction)
    # mesure = pred1.donnees
    mesure = Valeurs_Morgan()
    for instant in range(N_DEPART, N_RESULT + 1):
        nouv_valeur = Lecture_Nouvelle_Valeur(instant-1, mesure)
        vitesse_vent = Lecture_Nouvelle_Valeur_Vent(instant-1, mesure)
        # print("date mesure", nouv_valeur[1], nouv_valeur[2], "valeur : ",
        #       nouv_valeur[0], " prévu : ", resultat[0], "prévu filtré : ",
        #       resultat_filtre[0])
        # print("vvent : ", vitesse_vent)
        # resultat = pred1.Prediction(nouv_valeur)
        resultat = pred1.Prediction(nouv_valeur, vitesse_vent)
        date_mesure = pred1.Info_Date()
        tendance = pred1.Tendance()
        ecart_moyen = pred1.Ecart_Moyen(1)
        ecart_moyen_f = pred1.Ecart_Moyen_Filtre(1)
        ecart_tendance = pred1.Ecart_Tendance()
        # print("date mesure", date_mesure, " tendance : ", tendance,
        #       "h-1,h,h+1,h+2", histo[TAILLE_BUFFER-1], histo[TAILLE_BUFFER],
        #       resultat[0], resultat[1])
        print("date mesure", date_mesure, " tendance : ", tendance,
             "ecart moyen", ecart_moyen[0], "ecart moyenf", ecart_moyen_f[0],
             "ecart tendance ", ecart_tendance)
        # resultat_filtre = pred1.Prediction_Filtre(nouv_valeur, vitesse_vent)
        # print("resultat1", resultat)
        if instant % 100 == 0:
            print("instant : ", instant)
        if instant == N_RESULT:
            pred1.Debug_Pred()
    del pred1

Essai_Predicteur2()
