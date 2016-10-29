# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:07:02 2016
@author: Philippe
Methodes de la classe predicteur
"""

from datetime import datetime
from numpy import ones, zeros, load, save

from algorithme_prediction import AcquisitionBuffer, Mesure_Ecart_Meilleur,\
    Apprentissage_Prediction, Decalage_Buffer_Pred_Meilleur, \
    Meilleure_Prediction, Analyse
from affiche import Affiche_Buffer, Affiche_Donnees_Traitees, \
    Affiche_Analogie, Affiche_Parametre, Affiche_Prediction
from analogie import Mesure_Ecart_Analogie, Apprentissage_Analogie, \
    Decalage_Buffer_Pred_Analogie, Predicteur_Analogie
from parametre import Mesure_Ecart_Parametre, Decalage_Buffer_Pred_Parametre, \
    Predicteur_Parametre
from reference import Mesure_Ecart_Reference, Decalage_Buffer_Pred_Reference, \
    Predicteur_Reference
from bibliotheque import Init_Bibliotheque

from constante import ANNEE_POINT, FILTRE, HEURE_POINT, HORIZON, \
    JOUR_POINT, MOIS_POINT, NON_FILTRE, PRED_RESULTAT, TAILLE_BUFFER, \
    NB_PREDICTEURS, ANA_SCENARIO, C_MEM_ANA, C_MEM_PARAM, DEBUG_PREDICTION, \
    DEBUG_ANALOGIE, DEBUG_BUFFER, DEBUG_DONNEES, DEBUG_PARAMETRE, N_ATTRIBUT,\
    N_LIGNE, NB_SEQ, C_MEM_PREDICTION, REF_SCENARIO


class predicteur:
    """
    Methodes liees a la prediction de mesures sur la base d un historique de
    ces mesures.
    """

    def __init__(self, serie_a_traiter, reset_prediction):
        """
        Initialisation des donnees :
                initialisation des variables internes.
                chargement de la bibliotheque et des buffers

        Entrees :
           serie_a_traiter : Numero de la serie de mesure concernee
           reset_prediction : Booleen avec remise a zero des buffers si True
        """
        # donnees predicteur principal
        self.b_prediction_meilleur = zeros((TAILLE_BUFFER+1, HORIZON))
        self.b_pred_filtre = zeros((TAILLE_BUFFER+1, HORIZON))
        self.ecart_pred_meilleur = zeros((HORIZON))
        self.coef_predicteur = ones((HORIZON, NB_PREDICTEURS)) / NB_PREDICTEURS
        self.b_pred_tableau = zeros((TAILLE_BUFFER+1, 2, NB_PREDICTEURS,
                                     HORIZON))
        self.memoire_prediction = C_MEM_PREDICTION

        # donnees predicteur analogie
        self.b_prediction_analogie = zeros((TAILLE_BUFFER+1, ANA_SCENARIO,
                                            PRED_RESULTAT, HORIZON))
        self.ecart_pred_analogie = zeros((ANA_SCENARIO, PRED_RESULTAT,
                                          HORIZON))
        self.ecart_analogie_global = zeros((ANA_SCENARIO, PRED_RESULTAT))
        self.resultat_analogie = zeros((2, PRED_RESULTAT+1))
        self.memoire_analogie = C_MEM_ANA
        print(self.memoire_analogie[6, 7])
        self.memoire_moyenne_ana = zeros((ANA_SCENARIO))
        for i in range(ANA_SCENARIO):
            self.memoire_moyenne_ana[i] = (PRED_RESULTAT - 1) / 2
        self.horizon_pred = zeros((HORIZON))
        self.horizon_pred[0] = 1.0

        # donnees predicteur parametre
        self.b_prediction_parametre = zeros((TAILLE_BUFFER+1, PRED_RESULTAT,
                                             HORIZON))
        self.ecart_pred_parametre = zeros((PRED_RESULTAT, HORIZON))
        self.memoire_param = C_MEM_PARAM
        self.resultat_parametre = zeros((2, PRED_RESULTAT+1))

        # donnees predicteur references
        self.b_prediction_reference = zeros((TAILLE_BUFFER+1, REF_SCENARIO,
                                             HORIZON))
        self.ecart_reference = zeros((REF_SCENARIO, HORIZON))

        # donnees generales bibliotheque
        self.donnees = zeros((N_ATTRIBUT+1, N_LIGNE+1))
        self.min_max_seq = zeros((NB_SEQ+1, 2))
        Init_Bibliotheque(serie_a_traiter, self.donnees, self.min_max_seq)
        if DEBUG_DONNEES:
            Affiche_Donnees_Traitees(self.donnees)

        # donnees programme principal
        self.buffer = zeros((N_ATTRIBUT+1, TAILLE_BUFFER+1))
        self.buffer[ANNEE_POINT, TAILLE_BUFFER] = 1900
        self.buffer[MOIS_POINT, TAILLE_BUFFER] = 1
        self.buffer[JOUR_POINT, TAILLE_BUFFER] = 1
        self.buffer[HEURE_POINT, TAILLE_BUFFER] = 0
        self.serie = serie_a_traiter

        # rechargement des parametres de h-1
        if reset_prediction is False:
            nom_fichier = "serie" + str(serie_a_traiter)
            fichier = open(nom_fichier, "rb")
            self.b_prediction_reference = load(fichier)
            self.b_prediction_analogie = load(fichier)
            self.b_prediction_parametre = load(fichier)
            self.b_prediction_meilleur = load(fichier)
            self.b_pred_filtre = load(fichier)
            self.b_pred_tableau = load(fichier)
            self.coef_predicteur = load(fichier)
            self.memoire_moyenne_ana = load(fichier)
            self.buffer = load(fichier)
            fichier.close()

    def Prediction_Valeur(self, valeur_mesuree):
        """
            Methode interne de calcul des valeurs predites sans controles
            préalables (methode a ne pas appeler)

            entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
            sortie :
                Valeurs prédites de h+1 à h+ HORIZON
        """
        AcquisitionBuffer(valeur_mesuree, self.buffer,
                          self.b_prediction_meilleur)
        if DEBUG_BUFFER:
            Affiche_Buffer(self.buffer)

        # mesure des ecarts avec h-1 : ecart entre pred(h-1)
        # et buffer(taille)
        Mesure_Ecart_Reference(self.ecart_reference,
                               self.b_prediction_reference, self.buffer)
        Mesure_Ecart_Analogie(self.ecart_pred_analogie,
                              self.b_prediction_analogie,
                              self.ecart_analogie_global,
                              self.horizon_pred, self.buffer)
        Mesure_Ecart_Parametre(self.ecart_pred_parametre,
                               self.b_prediction_parametre,
                               self.horizon_pred, self.buffer)
        Mesure_Ecart_Meilleur(self.ecart_pred_meilleur,
                              self.b_prediction_meilleur, self.horizon_pred,
                              self.buffer)

        # affichage des donnees
        if DEBUG_ANALOGIE:
            Affiche_Analogie(self.buffer, self.b_prediction_analogie,
                             self.ecart_pred_analogie,
                             self.resultat_analogie,
                             self.ecart_analogie_global)
        if DEBUG_PARAMETRE:
            Affiche_Parametre(self.buffer, self.b_prediction_parametre,
                              self.ecart_pred_parametre,
                              self.resultat_parametre)
        if DEBUG_PREDICTION:
            Affiche_Prediction(self.b_prediction_reference,
                               self.coef_predicteur,
                               self.memoire_moyenne_ana,
                               self.b_prediction_analogie,
                               self.b_prediction_parametre,
                               self.b_prediction_meilleur,
                               self.ecart_pred_meilleur, self.buffer)

        # ajustement des parametres d apprentissage
        Apprentissage_Analogie(self.ecart_analogie_global,
                               self.memoire_moyenne_ana)
        Apprentissage_Prediction(self.ecart_reference,
                                 self.memoire_moyenne_ana,
                                 self.ecart_pred_analogie,
                                 self.ecart_pred_parametre,
                                 self.coef_predicteur,
                                 self.b_pred_tableau,
                                 self.memoire_prediction)

        # decalage des valeurs predites
        Decalage_Buffer_Pred_Reference(self.b_prediction_reference)
        Decalage_Buffer_Pred_Analogie(self.b_prediction_analogie)
        Decalage_Buffer_Pred_Parametre(self.b_prediction_parametre)
        Decalage_Buffer_Pred_Meilleur(self.b_pred_filtre,
                                      self.b_prediction_meilleur,
                                      self.b_pred_tableau)

        # calcul des valeurs predites pour instant
        # et instant + HORIZON
        Predicteur_Reference(self.b_prediction_reference,
                             self.b_prediction_meilleur, self.b_pred_filtre,
                             self.buffer, self.min_max_seq)
        Predicteur_Analogie(self.resultat_analogie, self.b_prediction_analogie,
                            self.memoire_analogie, self.donnees, self.buffer)
        Predicteur_Parametre(self.resultat_parametre,
                             self.b_prediction_parametre,
                             self.memoire_param, self.donnees, self.buffer)
        Meilleure_Prediction(self.b_pred_filtre, self.b_prediction_meilleur,
                             self.b_prediction_reference,
                             self.b_prediction_analogie,
                             self.b_prediction_parametre,
                             self.coef_predicteur, self.memoire_moyenne_ana,
                             self.buffer)

        # stockage des parametres
        nom_fichier = "serie" + str(self.serie)
        fichier = open(nom_fichier, "wb")
        save(fichier, self.b_prediction_reference)
        save(fichier, self.b_prediction_analogie)
        save(fichier, self.b_prediction_parametre)
        save(fichier, self.b_prediction_meilleur)
        save(fichier, self.b_pred_filtre)
        save(fichier, self.b_pred_tableau)
        save(fichier, self.coef_predicteur)
        save(fichier, self.memoire_moyenne_ana)
        save(fichier, self.buffer)
        fichier.close()

        # sortie des resultats
        resultat = self.b_prediction_meilleur[0, :]
        return resultat

    def Prediction(self, valeur_mesuree):
        """
            Calcul des valeurs predites :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, retourne la valeur
                actuelle
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                Valeur_mesurée : array avec annee, mois, jour, heure et valeur
            Sortie :
                Valeurs prédites : array de h+1 à h+HORIZON
        """
        resultat = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            resultat = self.Prediction_Valeur(valeur_mesuree)
        elif validation == 0:  # pas de recalcul
            resultat = self.b_prediction_meilleur[0, :]

        # pas de restitution si historique insuffisant
        if self.buffer[NON_FILTRE, TAILLE_BUFFER-4] == 0 and validation != -1:
            resultat = zeros((HORIZON))
        return resultat

    def Prediction_Filtre(self, valeur_mesuree):
        """
            Calcul des valeurs predites filtrees :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, pas de prediction
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
            Sortie :
                valeurs prédites filtrees : array de h+1 à h+HORIZON
        """
        resultat_filtre = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            resultat_filtre = self.Prediction_Valeur(valeur_mesuree)
        resultat_filtre = self.b_pred_filtre[0, :]

        # pas de restitution si historique insuffisant
        if self.buffer[NON_FILTRE, TAILLE_BUFFER-4] == 0 and validation != -1:
            resultat_filtre = zeros((HORIZON))
        return resultat_filtre

    def Info_Date(self):
        """
        Fourniture de la date de la dernière valeur aquise :
        Sortie :
            date_mesure : datetime de la dernière mesure h (prediction = h+1)
        """
        date_mesure = datetime(int(self.buffer[ANNEE_POINT, TAILLE_BUFFER]),
                               int(self.buffer[MOIS_POINT, TAILLE_BUFFER]),
                               int(self.buffer[JOUR_POINT, TAILLE_BUFFER]),
                               int(self.buffer[HEURE_POINT, TAILLE_BUFFER]))
        return date_mesure

    def Tendance(self):
        """
        Fourniture de l evolution des mesures :
            ecart entre la moyenne des 2 dernieres et des 2 prochaines heures
        Sortie :
            tendance : ecart des 2 dernieres
        """
        moyenne_actuelle = (self.buffer[NON_FILTRE, TAILLE_BUFFER] +
                            self.buffer[NON_FILTRE, TAILLE_BUFFER-1]) / 2
        moyenne_future = (self.b_prediction_meilleur[0, 0] +
                          self.b_prediction_meilleur[0, 1]) / 2
        tendance = moyenne_future - moyenne_actuelle
        return tendance

    def Historique(self):
        """
        Fourniture de l historique des mesures. La plus recente (TAILLE_BUFFER)
        correspond a la date fournie par Info_Date.

        Sortie :
            histo : array de 0 (ancien) a TAILLE_BUFFER (actuel)
        """
        histo = zeros((TAILLE_BUFFER+1))
        histo = self.buffer[NON_FILTRE, 0:TAILLE_BUFFER+1]
        return histo

    def Historique_Filtre(self):
        """
        Fourniture de l historique des mesures filtrees. La plus recente
        (TAILLE_BUFFER) correspond a la date fournie par Info_Date.
        La plus recente est calculee avec egalement la premiere estimation.

        Sortie :
            histo_filtre : array de 0 (ancien) a TAILLE_BUFFER (actuel)
        """
        histo_filtre = zeros((TAILLE_BUFFER+1))
        histo_filtre = self.buffer[FILTRE, 0:TAILLE_BUFFER+1]
        return histo_filtre

    def Ecart_Moyen(self, horizon):
        """
        Moyenne des ecarts absolus et relatif des 5 dernières predictions
        pour un horizon donne (1 par defaut).
        Ecart fourni uniquement si l historique est de 24h

        Entree :
            Horizon : horizon de prediction choisi (1 par defaut)
        Sortie :
            ecart_moyen : array avec 0 pour ecart absolu et 1 pour relatif
        """
        ecart_moyen = zeros((2))
        if self.buffer[NON_FILTRE, 0] > 0.1:
            for i in range(5):
                ecart_abs_i = abs(self.buffer[NON_FILTRE, TAILLE_BUFFER - i] -
                                  self.b_prediction_meilleur[horizon + i,
                                                             horizon - 1])
                ecart_relatif_i = ecart_abs_i / \
                    self.buffer[NON_FILTRE, TAILLE_BUFFER - i]
                ecart_moyen[0] += ecart_abs_i
                ecart_moyen[1] += ecart_relatif_i
            ecart_moyen[0] /= 5
            ecart_moyen[1] /= 5
        return ecart_moyen

    def Ecart_Moyen_Filtre(self, horizon):
        """
        Moyenne des ecarts absolus et relatif des 5 dernières predictions
        filtrees pour un horizon donne (1 par defaut).
        Ecart fourni uniquement si l historique est de 24h

        Entree :
            Horizon : horizon de prediction choisi (1 par defaut)
        Sortie :
            ecart_moyen : array avec 0 pour ecart absolu et 1 pour relatif
        """
        ecart_moyen_filtre = zeros((2))
        if self.buffer[NON_FILTRE, 0] > 0.1:
            for i in range(5):
                ecart_abs_i = abs(self.buffer[FILTRE, TAILLE_BUFFER - i] -
                                  self.b_pred_filtre[horizon + i, horizon - 1])
                ecart_relatif_i = ecart_abs_i / \
                    self.buffer[FILTRE, TAILLE_BUFFER - i]
                ecart_moyen_filtre[0] += ecart_abs_i
                ecart_moyen_filtre[1] += ecart_relatif_i
            ecart_moyen_filtre[0] /= 5
            ecart_moyen_filtre[1] /= 5
        return ecart_moyen_filtre

    def Ecart_Tendance(self):
        """
        Fourniture de la moyenne des écarts des 3 dernières tendances :
            ecart entre la tendance calculee sur les valeurs predites et
            la tendance calculee sur les valeurs reelles.
        Ecart fourni uniquement si l historique est de 24h

        Sortie :
            ecart : moyenne des 3 ecarts
        """
        ecart = 0.
        if self.buffer[NON_FILTRE, 0] > 0.1:
            for t in range(2, 5):
                prevu = (self.b_prediction_meilleur[t, 0] +
                         self.b_prediction_meilleur[t, 1]) / 2
                reel = (self.buffer[NON_FILTRE, TAILLE_BUFFER-t+1] +
                        self.buffer[NON_FILTRE, TAILLE_BUFFER-t+2]) / 2
                ecart += abs(prevu - reel)
            ecart /= 3
        return ecart
