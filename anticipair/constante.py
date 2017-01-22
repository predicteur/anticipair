#  -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 17:02:00 2016

@author: Philippe

Déclaration des constantes utilisées pour la classe prédicteur.
    partie 1 : parametres de simulation
    partie 2 : constantes générales non modifiables
    partie 3 : constantes ajustables (modifient le fonctionnement du programme)
    partie 4 : constantes deduites
    partie 5 : initialisation des valeurs des coefficients d ajustement
"""

from numpy import zeros, ones
from datetime import timedelta, datetime

#   parametres lies a la simulation

# simulation : parametres de reglage
T_BUFFER = 96  # taille du buffer pour les donnees acquises et predites
PARA_SENS = 1    # METTRE A -1 POUR LES SERIES O3 ET A 1 POUR LES AUTRES SERIES
HORIZON = 6    # horizon de prediction (nombre d heures predites)
ACTIVATION_REF = True    # activation predicteur de reference
ACTIVATION_ANA = True    # activation predicteur analogie
ACTIVATION_PARAM = True    # activation predicteur parametre
ACTIVATION_VENT = True    # activation predicteur vent
ACTIVATION_MODELE = True    # activation predicteur modele
ACTIVATION_MAUVAIS = False  # penalisation preds mauvais / algos optimisation
# simulation : affichage d'informations
DEBUG_DONNEES = False  # print des donnees
DEBUG_BUFFER = False  # print des buffer
DEBUG_ANALOGIE = False  # print des donnees analogie
DEBUG_PARAMETRE = False  # print des donnees parametre
DEBUG_REFERENCE = False  # print des donnees reference
DEBUG_VENT = False  # print des donnees vent
DEBUG_MODELE = False  # print des donnees modele
DEBUG_ALGO = False  # print des donnees algo
# simulation : export des donnees inermediaires dans un fichier
DEBUG_PREDICTION1 = True  # export des donnees predites h+1
DEBUG_PREDICTION2 = True  # export des donnees predites h+2
DEBUG_PREDICTION3 = True  # export des donnees predites h+3
DEBUG_PREDICTION4 = True  # export des donnees predites h+4
DEBUG_PREDICTION5 = True  # export des donnees predites h+5
DEBUG_PREDICTION6 = True  # export des donnees predites h+6
AFFICHE_HORIZON = 0    # horizon pour les print (0 a HORIZON-1)

#   constantes generales non modifiables (liees a la structure du programme)

# donnees fichier de debug
N_AFFICHE = 4000   # nombre de lignes a afficher -> prendre N_RESULT + 100
# donnees bibliotheque et buffer
N_ATTRIBUT = 11    # nombre d attributs pour les donnees et pour buffer
NON_FILTRE = 0    # valeur non filtrees
FILTRE = 1    # valeur filtrees
SEQUENCE = 2  # sequence(1 nuit 0-5, 2 matin 6-10, 3 midi 11-16, 4 soir 17-23)
DEB_NUIT = 0
NUIT = 1
DEB_MATIN = 6
MATIN = 2
DEB_MIDI = 11
MIDI = 3
DEB_SOIR = 17
SOIR = 4
TYPE_POINT = 3    # type de point (-1 mini, 1 maxi, 0 reste)
MIN_POINT = -1
MAX_POINT = 1
INTER_POINT = 0
HEURE_POINT = 4    # heure de la valeur
JOUR_POINT = 5    # jour de la valeur
MOIS_POINT = 6    # mois de la valeur
ANNEE_POINT = 7    # annee de la valeur
MIN_SEQ = 0    # mini de la sequence
MAX_SEQ = 1    # maxi de la sequence
NB_SEQ = 4    # nombre de sequences
V_VENT = 8    # valeur de la vitesse du vent
V_MODELE = 9    # valeur issue de la modelisation
ECART = 10    # ecart valeur de t moins valeur de t-1
ECRETE = 11    # valeur avec pic ecrete
# predicteur analogie
ANA_HEURE = 0    # heure du resultat
ANA_ECART_MC = 1    # ecart MC du resultat
ANA_V_VENT = 2    # vitesse du vent du resultat
# predicteur parametre
PARA_HEURE = 0    # heure du resultat
PARA_ECART_MC = 1    # ecart MC du resultat
PARA_V_VENT = 2    # vitesse du vent du resultat
# prediction
PRED_ECART = 0  # ecart prediction
PRED_RANG = 1    # rang prediction
NB_V_ALGO = 7    # nombre de parametres des algorithmes
N_PRED_MOYEN = 0    # vitesse prediction historique
N_ECART = 1    # vitesse prediction par ecart
N_MEMOIRE = 2    # vitesse prediction par ordre
N_PREDIC = 3    # vitesse prediction par meilleur1
N_PREDIC2 = 4    # vitesse prediction par meilleur2
N_PREDIC3 = 5    # vitesse prediction par meilleur3
N_PENAL = 6    # vitesse prediction par penalisation moins bon
# valeurs predites
VAL_ANNEE = 4
VAL_MOIS = 3
VAL_JOUR = 2
VAL_HEURE = 1
VAL_VALEUR = 0
DATE_INIT = datetime(1900, 1, 1, 0)
TIME_HEURE = timedelta(0, 3600)
MAXI = 10000000.0

#  constantes ajustables (modifient le fonctionnement du programme)

# predicteurs : parametres de reglage commun
BUF_SERIE = NON_FILTRE  # donnees pour buffer : ECRETE, FILTRE ou NON_FILTRE
BIB_SERIE = NON_FILTRE  # donnees pour biblio : ECRETE, FILTRE ou NON_FILTRE
SEUIL_ECRETAGE = 95  # % de limitation des ecarts (pics) pour l'option ECRETE
# predicteur vent : parametres de reglage
VENT_SCENARIO = 5    # nombre de predicteurs vent (idem PRED_RESULTAT)
VENT_MIN = 0.8    # seuil min vitesse vent (était 0,8)
VENT_MAX = 3.3    # seuil max vitesse vent (était 3,3)
VENT_PRED = True  # activation sur les valeurs prédites (false->dernières vals)
VENT_PARANA = True    # tri/vent des sequences testees pour pred para et ana
# predicteur modele : parametres de reglage
MODELE_SCENARIO = 5    # nombre de predicteurs modele (idem PRED_RESULTAT)
MODELE_MIN = 0.8    # seuil min valeur modele (était 0,8)
MODELE_PRED = True  # activation sur les valeurs prédites (false->derns vals)
# predicteur reference : parametres de reglage
REF_SCENARIO = 4    # nombre de predicteurs de reference
REF_PENTE = 1.0    # pente du predicteurs de reference (par défaut valeur 1)
REF_MOYENNE = T_BUFFER  # moyenne du predicteurs de reference
# predicteur analogie : parametres de reglage
PRED_RESULTAT = 5   # nombre de meilleurs candidats conserves pour ana et param
ANA_PROFONDEUR = 8    # nombre d heures de comparaison
ANA_SCENARIO = 8   # nombre de scenario de calcul d ecart traites
# predicteur parametre : parametres de reglage
PARA_PROFONDEUR = 3   # nombre de points de comparaison
PARA_HORIZON_POINT = 20   # horizon de recherche des points (< a T_BUFFER)
# predicteur algo : parametres de reglage
NB_ALGO = 20   # nombre d algorithmes d'optimisation
V_PRED_MOYEN = 1  # moyenne histo des rangs des prédicteurs (0 :h, 1 :h et h-1)
V_PENAL = 1.0   # vitesse evolution de la penalisation des mauvais predicteurs
V_MEMOIRE = 1.0    # vitesse d evolution - methode par ordre
V_ECART = 0.5    # vitesse d evolution - methode par ecart
V_PREDIC = 0.05    # vitesse d evolution de la prediction : etait (0,08)
V_PREDIC2 = 0.04    # vitesse d evolution de la prediction : etait (0,04)
V_PREDIC3 = 0.01    # vitesse d evolution de la prediction : etait (0,02)
V_MOYENNE = 0.3    # vitesse d evolution de la moyenne : etait 0.1
OPTI_ALGO = 2   # vitesse algo(1 : v=1/ecart, 2 : param mémoire, 3 : V_PREDIC)
NB_PRED_REDUIT = 15  # nombre de predicteurs conserves dans les algos
NB_ALGO_REDUIT = 18  # nombre de predicteurs de synthese pour l'estim finale
MAX_VARIATION = 1  # coef pour les variations maxi entre 2 valeurs successives
MAX_VALEUR = 3  # coefficient pour les valeurs maxi

# constantes déduite

NB_PREDICTEURS = REF_SCENARIO + ANA_SCENARIO + PRED_RESULTAT + VENT_SCENARIO +\
                 MODELE_SCENARIO  # nb des predicteurs
NB_ECART_PRED = NB_PREDICTEURS + NB_ALGO + 2  # nb total pred
I_REF = 0
I_ANA = I_REF + REF_SCENARIO
I_PARAM = I_ANA + ANA_SCENARIO
I_VENT = I_PARAM + PRED_RESULTAT
I_MODELE = I_VENT + VENT_SCENARIO
I_ALGO = I_MODELE + MODELE_SCENARIO
I_MEILLEUR = I_ALGO + NB_ALGO
DEBUG_PREDICTION = DEBUG_PREDICTION1 or DEBUG_PREDICTION2 or \
    DEBUG_PREDICTION3 or DEBUG_PREDICTION4 or DEBUG_PREDICTION5 or \
    DEBUG_PREDICTION6
N_COLONNE = NB_PREDICTEURS * NB_ALGO + 3 * NB_ALGO + 2 * MODELE_SCENARIO + \
    2 * VENT_SCENARIO + 2 * PRED_RESULTAT + 3 * ANA_SCENARIO + \
    2 * REF_SCENARIO + 13

# initialisation des valeurs des coefficients d ajustement

# initialisation des coefficients d ajustement des predicteurs
C_MEM_PREDICTION = zeros((NB_PREDICTEURS))
C_MEM_PREDICTION[0] = 0.15
C_MEM_PREDICTION[1] = 0.13
C_MEM_PREDICTION[2] = 0.11
C_MEM_PREDICTION[3] = 0.09
C_MEM_PREDICTION[4] = 0.08
C_MEM_PREDICTION[5] = 0.07
C_MEM_PREDICTION[6] = 0.06
C_MEM_PREDICTION[7] = 0.05
C_MEM_PREDICTION[8] = 0.05
C_MEM_PREDICTION[9] = 0.04
C_MEM_PREDICTION[10] = 0.04
C_MEM_PREDICTION[11] = 0.03
C_MEM_PREDICTION[12] = 0.03
C_MEM_PREDICTION[13] = 0.02
C_MEM_PREDICTION[14] = 0.02
C_MEM_PREDICTION[15] = 0.01
C_MEM_PREDICTION[16] = 0.01
C_MEM_PREDICTION[17] = 0.01
C_MEM_PREDICTION[18] = 0.0
C_MEM_PREDICTION[19] = 0.0
C_MEM_PREDICTION[20] = 0.0
# initialisation des coef memoire analogie
C_MEM_ANA = zeros((ANA_PROFONDEUR, ANA_SCENARIO))
C_MEM_ANA[0, 0] = 0.05
C_MEM_ANA[1, 0] = 0.05
C_MEM_ANA[2, 0] = 0.1
C_MEM_ANA[3, 0] = 0.1
C_MEM_ANA[4, 0] = 0.15
C_MEM_ANA[5, 0] = 0.15
C_MEM_ANA[6, 0] = 0.2  # 0,3 au lieu de 0,2
C_MEM_ANA[7, 0] = 0.2  # 0,1 au lieu de 0,2

C_MEM_ANA[0, 1] = 0.02
C_MEM_ANA[1, 1] = 0.03
C_MEM_ANA[2, 1] = 0.05
C_MEM_ANA[3, 1] = 0.1
C_MEM_ANA[4, 1] = 0.15
C_MEM_ANA[5, 1] = 0.15
C_MEM_ANA[6, 1] = 0.25  # 0,4 au lieu de 0,25
C_MEM_ANA[7, 1] = 0.25  # 0,1 au lieu de 0,25

C_MEM_ANA[0, 2] = 0.02
C_MEM_ANA[1, 2] = 0.03
C_MEM_ANA[2, 2] = 0.05
C_MEM_ANA[3, 2] = 0.07
C_MEM_ANA[4, 2] = 0.1
C_MEM_ANA[5, 2] = 0.15
C_MEM_ANA[6, 2] = 0.24
C_MEM_ANA[7, 2] = 0.34

C_MEM_ANA[0, 3] = 0.01
C_MEM_ANA[1, 3] = 0.02
C_MEM_ANA[2, 3] = 0.03
C_MEM_ANA[3, 3] = 0.05
C_MEM_ANA[4, 3] = 0.07
C_MEM_ANA[5, 3] = 0.1
C_MEM_ANA[6, 3] = 0.24
C_MEM_ANA[7, 3] = 0.48

C_MEM_ANA[0, 4] = 0.01
C_MEM_ANA[1, 4] = 0.01
C_MEM_ANA[2, 4] = 0.02
C_MEM_ANA[3, 4] = 0.02
C_MEM_ANA[4, 4] = 0.02
C_MEM_ANA[5, 4] = 0.05
C_MEM_ANA[6, 4] = 0.25
C_MEM_ANA[7, 4] = 0.62

C_MEM_ANA[0, 5] = 0.01
C_MEM_ANA[1, 5] = 0.01
C_MEM_ANA[2, 5] = 0.01
C_MEM_ANA[3, 5] = 0.01
C_MEM_ANA[4, 5] = 0.02
C_MEM_ANA[5, 5] = 0.02
C_MEM_ANA[6, 5] = 0.2
C_MEM_ANA[7, 5] = 0.72

C_MEM_ANA[0, 6] = 0.05
C_MEM_ANA[1, 6] = 0.05
C_MEM_ANA[2, 6] = 0.1
C_MEM_ANA[3, 6] = 0.1
C_MEM_ANA[4, 6] = 0.15
C_MEM_ANA[5, 6] = 0.15
C_MEM_ANA[6, 6] = 0.3
C_MEM_ANA[7, 6] = 0.1

C_MEM_ANA[0, 7] = 0.02
C_MEM_ANA[1, 7] = 0.03
C_MEM_ANA[2, 7] = 0.05
C_MEM_ANA[3, 7] = 0.1
C_MEM_ANA[4, 7] = 0.15
C_MEM_ANA[5, 7] = 0.25
C_MEM_ANA[6, 7] = 0.25
C_MEM_ANA[7, 7] = 0.15
# initialisation des coef memoire parametre
C_MEM_PARAM = zeros((PARA_PROFONDEUR))
C_MEM_PARAM[0] = 0.3
C_MEM_PARAM[1] = 0.5
C_MEM_PARAM[2] = 0.2
# initialisation des parametres des algorithmes
C_ALGO_PARAM = -ones((NB_ALGO, NB_V_ALGO))
for i in range(NB_ALGO):
    C_ALGO_PARAM[i, 0] = 0.0
    k = int(i / 2)
    C_ALGO_PARAM[2 * k, N_PENAL] = 1
C_ALGO_PARAM[0, N_ECART] = 0.5 * V_ECART
C_ALGO_PARAM[1, N_ECART] = 0.5 * V_ECART
C_ALGO_PARAM[2, N_ECART] = 1. * V_ECART
C_ALGO_PARAM[3, N_ECART] = 1. * V_ECART
C_ALGO_PARAM[4, N_ECART] = 1.2 * V_ECART
C_ALGO_PARAM[5, N_ECART] = 1.2 * V_ECART
C_ALGO_PARAM[6, N_MEMOIRE] = 0.5 * V_MEMOIRE
C_ALGO_PARAM[7, N_MEMOIRE] = 0.5 * V_MEMOIRE
C_ALGO_PARAM[8, N_MEMOIRE] = 1. * V_MEMOIRE
C_ALGO_PARAM[9, N_MEMOIRE] = 1. * V_MEMOIRE
C_ALGO_PARAM[10, N_MEMOIRE] = 2. * V_MEMOIRE
C_ALGO_PARAM[11, N_MEMOIRE] = 2. * V_MEMOIRE
C_ALGO_PARAM[12, N_PREDIC] = V_PREDIC
C_ALGO_PARAM[12, N_PREDIC2] = V_PREDIC2
C_ALGO_PARAM[12, N_PREDIC3] = V_PREDIC3
C_ALGO_PARAM[13, N_PREDIC] = V_PREDIC
C_ALGO_PARAM[13, N_PREDIC2] = V_PREDIC2
C_ALGO_PARAM[13, N_PREDIC3] = V_PREDIC3
C_ALGO_PARAM[14, N_PREDIC] = V_PREDIC
C_ALGO_PARAM[14, N_PREDIC2] = V_PREDIC2 - 0.01
C_ALGO_PARAM[14, N_PREDIC3] = V_PREDIC3 + 0.01
C_ALGO_PARAM[15, N_PREDIC] = V_PREDIC
C_ALGO_PARAM[15, N_PREDIC2] = V_PREDIC2 - 0.01
C_ALGO_PARAM[15, N_PREDIC3] = V_PREDIC3 + 0.01
C_ALGO_PARAM[16, N_PREDIC] = V_PREDIC - 0.01
C_ALGO_PARAM[16, N_PREDIC2] = V_PREDIC2 - 0.03
C_ALGO_PARAM[16, N_PREDIC3] = V_PREDIC3
C_ALGO_PARAM[17, N_PREDIC] = V_PREDIC - 0.01
C_ALGO_PARAM[17, N_PREDIC2] = V_PREDIC2 - 0.03
C_ALGO_PARAM[17, N_PREDIC3] = V_PREDIC3
C_ALGO_PARAM[18, N_PREDIC] = V_PREDIC - 0.02
C_ALGO_PARAM[18, N_PREDIC2] = V_PREDIC2 - 0.03
C_ALGO_PARAM[18, N_PREDIC3] = V_PREDIC3
C_ALGO_PARAM[19, N_PREDIC] = V_PREDIC - 0.02
C_ALGO_PARAM[19, N_PREDIC2] = V_PREDIC2 - 0.03
C_ALGO_PARAM[19, N_PREDIC3] = V_PREDIC3
