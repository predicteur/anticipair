# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:07:02 2016
@author: Philippe
Methodes de la classe predicteur
"""

from datetime import datetime
from numpy import ones, zeros, load, save

from algorithme_prediction import AcquisitionBuffer, Mesure_Ecart_Predicteur, \
    Apprentissage_Prediction, Decalage_Buffer_Pred_Meilleur, \
    Meilleure_Prediction, Analyse, Decalage_Buffer_Pred_Algo, \
    Apprentissage_Algorithme
from affiche import Affiche_Buffer, Affiche_Donnees_Traitees, \
    Affiche_Analogie, Affiche_Parametre, Affiche_Reference, \
    Affiche_Prediction, Affiche_Vent, Affiche_Algo, Affiche_Constante, \
    Affiche_Prediction_Complement
from analogie import Apprentissage_Analogie, Decalage_Buffer_Pred_Analogie, \
    Predicteur_Analogie
from parametre import Decalage_Buffer_Pred_Parametre, Predicteur_Parametre
from reference import Decalage_Buffer_Pred_Reference, Predicteur_Reference
from bibliotheque import Init_Bibliotheque
from vent import Predicteur_Correlation_Vent, Decalage_Buffer_Pred_Vent

from constante import ANNEE_POINT, FILTRE, HEURE_POINT, HORIZON, \
    JOUR_POINT, MOIS_POINT, NON_FILTRE, PRED_RESULTAT, TAILLE_BUFFER, \
    NB_PREDICTEURS, ANA_SCENARIO, C_MEM_ANA, C_MEM_PARAM, \
    DEBUG_ANALOGIE, DEBUG_BUFFER, DEBUG_DONNEES, DEBUG_PARAMETRE, N_ATTRIBUT,\
    N_LIGNE, NB_SEQ, C_MEM_PREDICTION, REF_SCENARIO, NB_ALGO, NB_ECART_PRED, \
    C_ALGO_PARAM, VENT_SCENARIO, DEBUG_REFERENCE, DEBUG_VENT, DEBUG_ALGO, \
    N_AFFICHE, N_COLONNE, FILE_DEBUG, DEBUG_PREDICTION2, DEBUG_PREDICTION3, \
    DEBUG_PREDICTION4, DEBUG_PREDICTION5, DEBUG_PREDICTION6


class predicteur:
    """
    Methodes liees a la prediction de mesures sur la base d un historique de
    ces mesures.
    """

    def __init__(self, serie_a_traiter, serie_vent, reset_prediction):
        """
        Initialisation des donnees :
                initialisation des variables internes.
                chargement de la bibliotheque et des buffers
        Entrees :
           serie_a_traiter : Numero de la serie de mesure concernee
           reset_prediction : Booleen avec remise a zero des buffers si True
        """
        # donnees predicteur principal
        self.b_pred_meilleur = zeros((TAILLE_BUFFER+1, HORIZON))
        self.b_pred_filtre = zeros((TAILLE_BUFFER+1, HORIZON))
        self.b_pred_algo = zeros((TAILLE_BUFFER+1, NB_ALGO, HORIZON))
        self.ecart_predicteur = zeros((NB_ECART_PRED, HORIZON))
        self.coef_predicteur = ones((HORIZON, NB_PREDICTEURS,
                                     NB_ALGO)) / NB_PREDICTEURS
        self.coef_algo = ones((HORIZON, NB_ALGO)) / NB_ALGO
        self.b_pred_tableau = zeros((TAILLE_BUFFER+1, 2, NB_PREDICTEURS,
                                     HORIZON))
        self.memoire_pred = C_MEM_PREDICTION
        self.algo_param = C_ALGO_PARAM

        # donnees predicteur vent
        self.b_pred_vent = zeros((TAILLE_BUFFER+1, VENT_SCENARIO, HORIZON))

        # donnees predicteur analogie
        self.b_pred_analogie = zeros((TAILLE_BUFFER+1, ANA_SCENARIO,
                                      PRED_RESULTAT, HORIZON))
        self.resultat_analogie = zeros((3, 2*PRED_RESULTAT+1))
        self.memoire_analogie = C_MEM_ANA
        # print(self.memoire_analogie[6, 7])
        self.memoire_moyenne_ana = ones((ANA_SCENARIO)) * \
            (PRED_RESULTAT - 1) / 2.0
        for i in range(ANA_SCENARIO):
            self.memoire_moyenne_ana[i] = (PRED_RESULTAT - 1) / 2.0
        self.horizon_pred = zeros((HORIZON))
        self.horizon_pred[0] = 1.0

        # donnees predicteur parametre
        self.b_pred_parametre = zeros((TAILLE_BUFFER+1, PRED_RESULTAT,
                                       HORIZON))
        self.ecart_pred_parametre = zeros((PRED_RESULTAT, HORIZON))
        self.memoire_param = C_MEM_PARAM
        self.resultat_parametre = zeros((3, 2*PRED_RESULTAT+1))

        # donnees predicteur references
        self.b_pred_reference = zeros((TAILLE_BUFFER+1, REF_SCENARIO, HORIZON))

        # donnees generales bibliotheque
        self.donnees = zeros((N_ATTRIBUT+1, N_LIGNE+1))
        self.min_max_seq = zeros((NB_SEQ+1, 2))
        Init_Bibliotheque(serie_a_traiter, serie_vent, self.donnees,
                          self.min_max_seq)
        # print('minmaxseq', self.min_max_seq)
        if DEBUG_DONNEES:
            Affiche_Donnees_Traitees(self.donnees)

        # donnees programme principal
        self.buffer = zeros((N_ATTRIBUT+1, TAILLE_BUFFER+1))
        self.buffer[ANNEE_POINT, TAILLE_BUFFER] = 1900
        self.buffer[MOIS_POINT, TAILLE_BUFFER] = 1
        self.buffer[JOUR_POINT, TAILLE_BUFFER] = 1
        self.buffer[HEURE_POINT, TAILLE_BUFFER] = 0
        self.serie = serie_a_traiter

        # donnees a stocker pour debug
        self.mat_affic = zeros((HORIZON, N_AFFICHE+1, N_COLONNE+1))
        self.mat_entete = zeros((N_COLONNE+1), dtype='a15')
        self.instant = 1

        # rechargement des parametres de h-1
        if reset_prediction is False:
            nom_fichier = "serie" + str(self.serie)
            fichier = open(nom_fichier, "rb")
            self.b_pred_reference = load(fichier)
            self.b_pred_analogie = load(fichier)
            self.b_pred_parametre = load(fichier)
            self.b_pred_vent = load(fichier)
            self.b_pred_algo = load(fichier)
            self.b_pred_meilleur = load(fichier)
            self.b_pred_filtre = load(fichier)
            self.b_pred_tableau = load(fichier)
            self.coef_predicteur = load(fichier)
            self.coef_algo = load(fichier)
            self.memoire_moyenne_ana = load(fichier)
            self.buffer = load(fichier)
            fichier.close()

    def Prediction_Valeur(self, valeur_mesuree, vitesse_vent):
        """
            Methode interne de calcul des valeurs predites sans controles
            préalables (methode a ne pas appeler)

            entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
                vitesse-vent : array de [0] a [HORIZON]
            sortie :
                Valeurs prédites de h+1 à h+ HORIZON
        """
        desactiv_vent = False
        if all(vitesse_vent == -1.0):
            desactiv_vent = True

        AcquisitionBuffer(valeur_mesuree, vitesse_vent, self.buffer,
                          self.b_pred_meilleur)
        if DEBUG_BUFFER:
            Affiche_Buffer(self.buffer)

        # mesure des ecarts avec h-1 : ecart entre pred(h-1) et buffer(taille)
        Apprentissage_Analogie(self.horizon_pred, self.b_pred_analogie,
                               self.memoire_moyenne_ana, self.buffer)
        Mesure_Ecart_Predicteur(self.ecart_predicteur, self.b_pred_algo,
                                self.b_pred_vent, self.b_pred_reference,
                                self.b_pred_analogie, self.b_pred_parametre,
                                self.b_pred_meilleur, self.b_pred_filtre,
                                self.buffer, self.memoire_moyenne_ana)

        # affichage des donnees
        if DEBUG_ANALOGIE:
            Affiche_Analogie(self.buffer, self.b_pred_analogie,
                             self.ecart_predicteur)
        if DEBUG_PARAMETRE:
            Affiche_Parametre(self.buffer, self.b_pred_parametre,
                              self.ecart_predicteur)
        if DEBUG_REFERENCE:
            Affiche_Reference(self.buffer, self.b_pred_reference,
                              self.ecart_predicteur)
        if DEBUG_VENT:
            Affiche_Vent(self.buffer, self.b_pred_vent, self.ecart_predicteur)
        if DEBUG_ALGO:
            Affiche_Algo(self.buffer, self.b_pred_algo, self.coef_algo,
                         self.ecart_predicteur)
        self.instant += 1
        Affiche_Prediction(self.instant, self.mat_affic, self.mat_entete,
                           self.b_pred_vent, self.b_pred_reference,
                           self.coef_predicteur, self.memoire_moyenne_ana,
                           self.b_pred_analogie,
                           self.b_pred_parametre, self.b_pred_filtre,
                           self.b_pred_meilleur, self.buffer,
                           self.b_pred_tableau, self.ecart_predicteur,
                           self.b_pred_algo, self.coef_algo)

        # ajustement des parametres d apprentissage
        Apprentissage_Prediction(self.ecart_predicteur,
                                 self.coef_predicteur, self.b_pred_tableau,
                                 self.memoire_pred, self.algo_param,
                                 desactiv_vent)
        Apprentissage_Algorithme(self.ecart_predicteur, self.coef_algo,
                                 self.memoire_pred)

        # decalage des valeurs predites
        Decalage_Buffer_Pred_Vent(self.b_pred_vent)
        Decalage_Buffer_Pred_Reference(self.b_pred_reference)
        Decalage_Buffer_Pred_Analogie(self.b_pred_analogie)
        Decalage_Buffer_Pred_Parametre(self.b_pred_parametre)
        Decalage_Buffer_Pred_Algo(self.b_pred_algo)
        Decalage_Buffer_Pred_Meilleur(self.b_pred_filtre,
                                      self.b_pred_meilleur,
                                      self.b_pred_tableau)

        # calcul des valeurs predites pour instant et instant + HORIZON
        Predicteur_Correlation_Vent(self.b_pred_vent, self.b_pred_meilleur,
                                    vitesse_vent, self.buffer)
        Predicteur_Reference(self.b_pred_reference,
                             self.b_pred_meilleur, self.b_pred_filtre,
                             self.buffer, self.min_max_seq)
        Predicteur_Analogie(self.resultat_analogie, self.b_pred_analogie,
                            self.memoire_analogie, self.donnees, self.buffer,
                            vitesse_vent, desactiv_vent)
        Predicteur_Parametre(self.resultat_parametre, self.b_pred_parametre,
                             self.memoire_param, self.donnees, self.buffer,
                             vitesse_vent, desactiv_vent)
        Meilleure_Prediction(self.b_pred_algo, self.b_pred_filtre,
                             self.b_pred_vent, self.b_pred_meilleur,
                             self.b_pred_reference, self.b_pred_analogie,
                             self.b_pred_parametre, self.coef_algo,
                             self.coef_predicteur, self.memoire_moyenne_ana,
                             self.buffer)
        Affiche_Prediction_Complement(self.instant, self.mat_affic,
                                      self.Tendance(), self.Ecart_Tendance(),
                                      self.Ecart_Moyen(),
                                      self.Ecart_Moyen_Filtre())

        # stockage des parametres
        nom_fichier = "serie" + str(self.serie)
        fichier = open(nom_fichier, "wb")
        save(fichier, self.b_pred_reference)
        save(fichier, self.b_pred_analogie)
        save(fichier, self.b_pred_parametre)
        save(fichier, self.b_pred_vent)
        save(fichier, self.b_pred_algo)
        save(fichier, self.b_pred_meilleur)
        save(fichier, self.b_pred_filtre)
        save(fichier, self.b_pred_tableau)
        save(fichier, self.coef_predicteur)
        save(fichier, self.coef_algo)
        save(fichier, self.memoire_moyenne_ana)
        save(fichier, self.buffer)
        fichier.close()

        # sortie des resultats
        resultat = self.b_pred_meilleur[0, :]
        return resultat

    def Prediction(self, valeur_mesuree, vitesse_vent=-ones((HORIZON + 1))):
        """
            Calcul des valeurs predites :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, retourne la valeur
                actuelle
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                Valeur_mesurée : array avec annee, mois, jour, heure et valeur
                vitesse-vent : optionnel, array de [0] a [HORIZON]
            Sortie :
                Valeurs prédites : array de h+1 à h+HORIZON
        """
        resultat = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            resultat = self.Prediction_Valeur(valeur_mesuree, vitesse_vent)
        elif validation == 0:  # pas de recalcul
            resultat = self.b_pred_meilleur[0, :]

        # pas de restitution si historique insuffisant
        if self.buffer[NON_FILTRE, TAILLE_BUFFER-4] == 0 and validation != -1:
            resultat = zeros((HORIZON))
        return resultat

    def Prediction_Filtre(self, valeur_mesuree, vitesse_vent):
        """
            Calcul des valeurs predites filtrees :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, pas de prediction
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
                vitesse-vent : optionnel, array de [0] a [HORIZON]
            Sortie :
                valeurs prédites filtrees : array de h+1 à h+HORIZON
        """
        resultat_filtre = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            resultat_filtre = self.Prediction_Valeur(valeur_mesuree,
                                                     vitesse_vent)
            resultat_filtre = self.b_pred_filtre[0, :]
        elif validation == 0:
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
                            self.buffer[NON_FILTRE, TAILLE_BUFFER-1]) / 2.0
        moyenne_future = (self.b_pred_meilleur[0, 0] +
                          self.b_pred_meilleur[0, 1]) / 2.0
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

    def Ecart_Moyen(self, horizon=1):
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
                ecart_abs_i = abs(self.buffer[NON_FILTRE, TAILLE_BUFFER-i] -
                                  self.b_pred_meilleur[horizon+i, horizon-1])
                ecart_relatif_i = ecart_abs_i / \
                    self.buffer[NON_FILTRE, TAILLE_BUFFER - i]
                ecart_moyen[0] += ecart_abs_i
                ecart_moyen[1] += ecart_relatif_i
            ecart_moyen[0] /= 5.0
            ecart_moyen[1] /= 5.0
        return ecart_moyen

    def Ecart_Moyen_Filtre(self, horizon=1):
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
            ecart_moyen_filtre[0] /= 5.0
            ecart_moyen_filtre[1] /= 5.0
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
        ecart = 0.0
        if self.buffer[NON_FILTRE, 0] > 0.1:
            for t in range(2, 5):
                prevu = (self.b_pred_meilleur[t, 0] +
                         self.b_pred_meilleur[t, 1]) / 2.0
                reel = (self.buffer[NON_FILTRE, TAILLE_BUFFER-t+1] +
                        self.buffer[NON_FILTRE, TAILLE_BUFFER-t+2]) / 2.0
                ecart += abs(prevu - reel)
            ecart /= 3.0
        return ecart

    def Debug_Pred(self):
        """
        Affichage des valeurs pour chaque pas de temps
        Sortie :
            écriture dans le fichier de debug
        """

        for k in range(HORIZON):
            fichier = FILE_DEBUG + str(k) + '.csv'
            if (k == 0) or \
               (k == 1 and DEBUG_PREDICTION2) or \
               (k == 2 and DEBUG_PREDICTION3) or \
               (k == 3 and DEBUG_PREDICTION4) or \
               (k == 4 and DEBUG_PREDICTION5) or \
               (k == 5 and DEBUG_PREDICTION6):

                # parametres principaux en premiere ligne
                with open(fichier, 'w') as fic:
                    ligne = Affiche_Constante(self.serie)
                    ligne += "\n"
                    fic.write(ligne)
                    fic.write('  ' + '\n')

                    # entete des colonnes
                    ligne = '  '
                    for col in range(1, N_COLONNE):
                        texte = str(self.mat_entete[col])
                        ligne += texte[2:len(texte)-1] + ';'
                    ligne += '\n' + '\n'
                    fic.write(ligne)

                    # resultats par ligne
                    for lig in range(N_AFFICHE):
                        ligne = '  '
                        for col in range(1, N_COLONNE):
                            ligne += str(self.mat_affic[k, lig, col]
                                         ).replace(".", ",") + ';'
                        ligne += '\n'
                        fic.write(ligne)
        return
