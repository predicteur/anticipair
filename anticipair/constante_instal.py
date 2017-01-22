#  -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 17:02:00 2016

@author: Philippe

Déclaration des fichiers importes pour le module bibiotheque et
des fichiers d'ecriture (si activation d'une option DEBUG_xxx)

Fichiers bibliotheque :
    fichiers CSV avec séparateur ";" et premiere ligne non importee (titre)
    Les 4 premières colonnes contiennent : annee, mois, jour, heure
    Les colonnes suivantes contiennent les serie de donnees

Fichier d'ecriture :
    Seul le chemin relatif + nom_fichier est a donner,
    un chiffre est ajouté au nom de fichier pour indiquer l'horizon de
    prediction (0 pour t+1, ..., 5 pour t+6).
    Le fichier est écrasé à chaque simulation.
"""

import os

# bibliotheque : historique des donnees

# si fichier Morgan
# FILE_BIBLIO = os.path.join("data", "apprentissage_Morgan.csv")
# N_LIGNE = 13866    # nombre de lignes du fichiers (donnees bibliotheque)
PCCINQ_MORGAN = 4  # colonne de la serie
VV1_MORGAN = 5  # colonne de la serie
VV2_MORGAN = 6  # colonne de la serie

# si fichier general
FILE_BIBLIO = os.path.join("data", "Biblio_2014-2015_export.csv")
N_LIGNE = 17520    # nombre de lignes du fichiers (donnees bibliotheque)
N2AIXA = 4  # colonne de la serie
N2AIXC = 5  # colonne de la serie
N2CINQ = 6  # colonne de la serie
N2PLOM = 7  # colonne de la serie
N2RABA = 8  # colonne de la serie
N2STLO = 9  # colonne de la serie
O3AIXA = 10  # colonne de la serie
O3AIXP = 11  # colonne de la serie
O3CINQ = 12  # colonne de la serie
PCAIXA = 13  # colonne de la serie
PCAIXC = 14  # colonne de la serie
PCCINQ = 15  # colonne de la serie
PCRABA = 16  # colonne de la serie
PCSTLO = 17  # colonne de la serie
AIXVV = 18  # colonne de la serie

# fichier de debug des donnees
FILE_DEBUG = "debug_prediction"
