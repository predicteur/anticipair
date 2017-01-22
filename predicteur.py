# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:07:02 2016
@author: Philippe
Methodes de la classe predicteur
"""

from datetime import datetime
from numpy import ones, zeros, load, save, arange, loadtxt

from algorithme_prediction import AcquisitionBuffer, Mesure_Ecart_Predicteur, \
    Apprentissage_Prediction, Meilleure_Prediction, Analyse, \
    Apprentissage_Algorithme
from affiche import Affiche_Buffer, Affiche_Donnees_Traitees, \
    Affiche_Analogie, Affiche_Parametre, Affiche_Reference, \
    Affiche_Prediction, Affiche_Vent, Affiche_Algo, Affiche_Constante, \
    Affiche_Prediction_Complement, Affiche_Modele
from analogie import Apprentissage_Analogie, Predicteur_Analogie
from parametre import Predicteur_Parametre
from reference import Predicteur_Reference
from bibliotheque import Init_Bibliotheque
from vent import Predicteur_Correlation_Vent
from modele import Predicteur_Correlation_Modele

from constante_instal import FILE_BIBLIO, FILE_DEBUG

from constante import ANNEE_POINT, FILTRE, HEURE_POINT, HORIZON, \
    JOUR_POINT, MOIS_POINT, NON_FILTRE, PRED_RESULTAT, T_BUFFER, \
    NB_PREDICTEURS, ANA_SCENARIO, C_MEM_ANA, C_MEM_PARAM, MODELE_SCENARIO, \
    DEBUG_ANALOGIE, DEBUG_BUFFER, DEBUG_DONNEES, DEBUG_PARAMETRE, N_ATTRIBUT,\
    NB_SEQ, C_MEM_PREDICTION, REF_SCENARIO, NB_ALGO, NB_ECART_PRED, \
    C_ALGO_PARAM, VENT_SCENARIO, DEBUG_REFERENCE, DEBUG_VENT, DEBUG_ALGO, \
    N_AFFICHE, N_COLONNE, DEBUG_PREDICTION2, DEBUG_PREDICTION3, \
    DEBUG_PREDICTION4, DEBUG_PREDICTION5, DEBUG_PREDICTION6, DEBUG_MODELE, \
    DEBUG_PREDICTION1, DEBUG_PREDICTION, I_REF, I_ANA, I_PARAM, I_VENT, \
    I_MODELE, I_ALGO, MAXI, V_VENT


class predicteur:
    """
    Methodes liees a la prediction de mesures sur la base d un historique de
    ces mesures.
    L'utilisation de cette classe nécessite de declarer des fichiers d'entree
    et de sortie dans le fichier "constante_instal.py".
    Les parametres de reglage de la classe sont definis dans le fichier
    "constante.py".

    """

    def __init__(self, serie_a_traiter, reset_prediction, serie_vent=-1):
        """
        Initialisation des donnees :
                initialisation des variables internes.
                chargement de la bibliotheque et des buffers
        Entrees :
           serie_a_traiter : Numero de la serie de mesure concernee
           reset_prediction : Booleen avec remise a zero des buffers si True
           serie_vent : Numero de la serie des mesures de vent (optionnel)
        """
        # donnees predicteur principal
        self.b_pred_meil = zeros((T_BUFFER+1, HORIZON))
        self.b_pred_filt = zeros((T_BUFFER+1, HORIZON))
        self.b_pred_algo = zeros((T_BUFFER+1, NB_ALGO, HORIZON))
        self.b_pred_unit = zeros((T_BUFFER+1, NB_PREDICTEURS, HORIZON))
        self.ecart_pred = zeros((NB_ECART_PRED, HORIZON))
        self.coef_pred = ones((HORIZON, NB_PREDICTEURS, NB_ALGO)) / \
            NB_PREDICTEURS
        self.coef_algo = ones((HORIZON, NB_ALGO)) / NB_ALGO
        self.b_pred_tab = zeros((T_BUFFER+1, 2, NB_PREDICTEURS, HORIZON))
        self.mem_pred = C_MEM_PREDICTION
        self.algo_param = C_ALGO_PARAM

        # donnees predicteur modele
        self.b_pred_mod = zeros((T_BUFFER+1, MODELE_SCENARIO, HORIZON))

        # donnees predicteur vent
        self.b_pred_vent = zeros((T_BUFFER+1, VENT_SCENARIO, HORIZON))

        # donnees predicteur analogie
        self.b_pred_ana = zeros((T_BUFFER+1, ANA_SCENARIO, PRED_RESULTAT,
                                 HORIZON))
        self.res_ana = zeros((3, 2*PRED_RESULTAT+1))
        self.mem_ana = C_MEM_ANA
        self.mem_moy_ana = ones((ANA_SCENARIO)) * (PRED_RESULTAT - 1) / 2.0
        for i in range(ANA_SCENARIO):
            self.mem_moy_ana[i] = (PRED_RESULTAT - 1) / 2.0
        self.h_pred = zeros((HORIZON))
        self.h_pred[0] = 1.0

        # donnees predicteur parametre
        self.b_pred_param = zeros((T_BUFFER+1, PRED_RESULTAT, HORIZON))
        self.mem_param = C_MEM_PARAM
        self.res_param = zeros((3, 2*PRED_RESULTAT+1))

        # donnees predicteur references
        self.b_pred_ref = zeros((T_BUFFER+1, REF_SCENARIO, HORIZON))

        # donnees generales bibliotheque
        bibli = loadtxt(FILE_BIBLIO, dtype='str', delimiter=',', skiprows=1)
        self.donnees = zeros((N_ATTRIBUT+1, bibli.size+1))
        self.min_max_seq = zeros((NB_SEQ+1, 2))
        self.seuil = Init_Bibliotheque(serie_a_traiter, serie_vent,
                                       self.donnees, self.min_max_seq)
        if DEBUG_DONNEES:
            Affiche_Donnees_Traitees(self.donnees)

        # donnees programme principal
        self.buffer = zeros((N_ATTRIBUT+1, T_BUFFER+1))
        self.buffer[ANNEE_POINT, T_BUFFER] = 1900
        self.buffer[MOIS_POINT, T_BUFFER] = 1
        self.buffer[JOUR_POINT, T_BUFFER] = 1
        self.buffer[HEURE_POINT, T_BUFFER] = 0
        self.serie = serie_a_traiter

        # donnees a stocker pour debug
        self.mat_affic = zeros((HORIZON, N_AFFICHE+1, N_COLONNE+1))
        self.mat_entete = zeros((N_COLONNE+1), dtype='a15')
        self.instant = 1

        # rechargement des parametres de h-1
        if reset_prediction is False:
            nom_fichier = "serie" + str(self.serie)
            fichier = open(nom_fichier, "rb")
            self.buffer = load(fichier)
            self.b_pred_unit = load(fichier)
            self.b_pred_ref = load(fichier)
            self.b_pred_ana = load(fichier)
            self.b_pred_param = load(fichier)
            self.b_pred_vent = load(fichier)
            self.b_pred_mod = load(fichier)
            self.b_pred_algo = load(fichier)
            self.b_pred_meil = load(fichier)
            self.b_pred_filt = load(fichier)
            self.b_pred_tab = load(fichier)
            self.coef_pred = load(fichier)
            self.coef_algo = load(fichier)
            self.mem_moy_ana = load(fichier)
            fichier.close()

    def Prediction_Valeur(self, valeur_mesuree, vitesse_vent, modele):
        """
            Methode interne de calcul des valeurs predites sans controles
            préalables (methode a ne pas appeler)

            entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
                vitesse-vent : array de [0] a [HORIZON]
                modele : array de [0] a [HORIZON]
            sortie :
                Valeurs prédites de h+1 à h+ HORIZON
        """
        desactiv_vent = all(vitesse_vent == -1.0) or \
            self.donnees[V_VENT, 1] < -0.5
        desactiv_modele = all(modele == -1.0)

        AcquisitionBuffer(valeur_mesuree, vitesse_vent, modele, self.buffer,
                          self.b_pred_meil, self.seuil)
        if DEBUG_BUFFER:
            Affiche_Buffer(self.buffer)

        # mesure des ecarts avec h-1 : ecart entre pred(h-1) et buffer(taille)
        Apprentissage_Analogie(self.h_pred, self.b_pred_ana,
                               self.mem_moy_ana, self.buffer)
        Mesure_Ecart_Predicteur(self.ecart_pred, self.b_pred_algo,
                                self.b_pred_unit, self.b_pred_meil,
                                self.b_pred_filt, self.buffer)
        # affichage des donnees
        if DEBUG_ANALOGIE:
            Affiche_Analogie(self.buffer, self.b_pred_ana, self.ecart_pred)
        if DEBUG_PARAMETRE:
            Affiche_Parametre(self.buffer, self.b_pred_param, self.ecart_pred)
        if DEBUG_REFERENCE:
            Affiche_Reference(self.buffer, self.b_pred_ref, self.ecart_pred)
        if DEBUG_VENT:
            Affiche_Vent(self.buffer, self.b_pred_vent, self.ecart_pred)
        if DEBUG_MODELE:
            Affiche_Modele(self.buffer, self.b_pred_mod, self.ecart_pred)
        if DEBUG_ALGO:
            Affiche_Algo(self.buffer, self.b_pred_algo, self.coef_algo,
                         self.ecart_pred)
        self.instant += 1
        if DEBUG_PREDICTION:
            Affiche_Prediction(self.instant, self.mat_affic, self.mat_entete,
                               self.b_pred_mod, self.b_pred_vent,
                               self.b_pred_ref, self.coef_pred,
                               self.mem_moy_ana, self.b_pred_ana,
                               self.b_pred_param, self.b_pred_filt,
                               self.b_pred_meil, self.buffer, self.b_pred_tab,
                               self.ecart_pred, self.b_pred_algo,
                               self.coef_algo)

        # ajustement des parametres d apprentissage
        Apprentissage_Prediction(self.ecart_pred, self.coef_pred,
                                 self.b_pred_tab, self.mem_pred,
                                 self.algo_param, desactiv_vent,
                                 desactiv_modele, self.b_pred_unit,
                                 self.buffer)
        Apprentissage_Algorithme(self.ecart_pred, self.coef_algo,
                                 self.mem_pred, self.buffer, self.b_pred_algo)

        # decalage des valeurs predites
        self.b_pred_unit = self.b_pred_unit[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_mod = self.b_pred_mod[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_vent = self.b_pred_vent[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_algo = self.b_pred_algo[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_filt = self.b_pred_filt[arange(-1, T_BUFFER-1), :]
        self.b_pred_ref = self.b_pred_ref[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_ana = self.b_pred_ana[arange(-1, T_BUFFER-1), :, :, :]
        self.b_pred_param = self.b_pred_param[arange(-1, T_BUFFER-1), :, :]
        self.b_pred_meil = self.b_pred_meil[arange(-1, T_BUFFER-1), :]
        self.b_pred_tab = self.b_pred_tab[arange(-1, T_BUFFER-1), :, :, :]

        # calcul des valeurs predites pour instant et instant + HORIZON
        self.b_pred_unit[0, I_REF:I_ANA, :] = \
            Predicteur_Reference(self.b_pred_ref, self.b_pred_meil,
                                 self.b_pred_filt, self.buffer,
                                 self.min_max_seq)
        self.b_pred_unit[0, I_ANA:I_PARAM, :] = \
            Predicteur_Analogie(self.res_ana, self.b_pred_ana, self.mem_ana,
                                self.donnees, self.buffer, vitesse_vent,
                                desactiv_vent, self.mem_moy_ana,
                                self.min_max_seq)
        self.b_pred_unit[0, I_PARAM:I_VENT, :] = \
            Predicteur_Parametre(self.res_param, self.b_pred_param,
                                 self.mem_param, self.donnees, self.buffer,
                                 vitesse_vent, desactiv_vent, self.min_max_seq)
        if desactiv_vent:
            self.b_pred_unit[0, I_VENT:I_MODELE, :] = ones((VENT_SCENARIO,
                                                            HORIZON))*MAXI
        else:
            self.b_pred_unit[0, I_VENT:I_MODELE, :] = \
                Predicteur_Correlation_Vent(self.b_pred_vent,
                                            self.b_pred_meil, vitesse_vent,
                                            self.buffer, self.min_max_seq)
        if desactiv_modele:
            self.b_pred_unit[0, I_MODELE:I_ALGO, :] = ones((MODELE_SCENARIO,
                                                            HORIZON))*MAXI
        else:
            self.b_pred_unit[0, I_MODELE:I_ALGO, :] = \
                Predicteur_Correlation_Modele(self.b_pred_mod,
                                              self.b_pred_meil, modele,
                                              self.buffer, self.min_max_seq)
        Meilleure_Prediction(self.b_pred_algo, self.b_pred_filt,
                             self.b_pred_unit, self.b_pred_meil,
                             self.coef_algo, self.coef_pred, self.buffer,
                             self.min_max_seq)

        # affichage des donnees dans le fichier csv
        if DEBUG_PREDICTION1:
            Affiche_Prediction_Complement(self.instant, self.mat_affic,
                                          self.Tendance(),
                                          self.Ecart_Tendance(),
                                          self.Ecart_Moyen(),
                                          self.Ecart_Moyen_Filtre())
        # stockage des parametres
        nom_fichier = "serie" + str(self.serie)
        fichier = open(nom_fichier, "wb")
        save(fichier, self.buffer)
        save(fichier, self.b_pred_unit)
        save(fichier, self.b_pred_ref)
        save(fichier, self.b_pred_ana)
        save(fichier, self.b_pred_param)
        save(fichier, self.b_pred_vent)
        save(fichier, self.b_pred_mod)
        save(fichier, self.b_pred_algo)
        save(fichier, self.b_pred_meil)
        save(fichier, self.b_pred_filt)
        save(fichier, self.b_pred_tab)
        save(fichier, self.coef_pred)
        save(fichier, self.coef_algo)
        save(fichier, self.mem_moy_ana)
        fichier.close()

        # sortie des resultats
        resultat = self.b_pred_meil[0, :]
        return resultat

    def Prediction(self, valeur_mesuree, vitesse_vent=-ones((HORIZON + 1)),
                   modele=-ones((HORIZON + 1))):
        """
            Calcul des valeurs predites :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, retourne la valeur
                actuelle
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                Valeur_mesurée : array avec annee, mois, jour, heure et valeur
                vitesse-vent : optionnel, array de [0] a [HORIZON] prevu
                modele : optionnel, array de [0] a [HORIZON] prevu
            Sortie :
                Valeurs prédites : array de [0] a [HORIZON]
        """
        res = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            res = self.Prediction_Valeur(valeur_mesuree, vitesse_vent, modele)
        elif validation == 0:  # pas de recalcul
            res = self.b_pred_meil[0, :]

        # pas de restitution si historique insuffisant
        if self.buffer[NON_FILTRE, T_BUFFER-4] == 0 and validation != -1:
            res = zeros((HORIZON))
        return res

    def Prediction_Filtre(self, valeur_mesuree,
                          vitesse_vent=-ones((HORIZON + 1)),
                          modele=-ones((HORIZON + 1))):
        """
            Calcul des valeurs predites filtrees :
                si les données d'entree sont incohérentes, retourne - 1
                si les données d'entree sont actuelles, pas de prediction
                si l'historique n'est pas suffisant (5 valeurs), retourne 0
            Entree :
                valeur_mesuree : array avec annee, mois, jour, heure et valeur
                vitesse-vent : optionnel, array de [0] a [HORIZON]
                modele : optionnel, array de [0] a [HORIZON]
            Sortie :
                valeurs prédites filtrees : array de [0] a [HORIZON]
        """
        resf = -ones((HORIZON))

        # lancement de la prediction si besoin
        validation = Analyse(valeur_mesuree, self.buffer)
        if validation == 1:
            resf = self.Prediction_Valeur(valeur_mesuree, vitesse_vent, modele)
            resf = self.b_pred_filt[0, :]
        elif validation == 0:
            resf = self.b_pred_filt[0, :]

        # pas de restitution si historique insuffisant
        if self.buffer[NON_FILTRE, T_BUFFER-4] == 0 and validation != -1:
            resf = zeros((HORIZON))
        return resf

    def Info_Date(self):
        """
        Fourniture de la date de la dernière valeur acquise :
        Entree :
            aucune
        Sortie :
            date_mesure : datetime de la dernière mesure h (prediction = h+1)
        """
        date_mesure = datetime(int(self.buffer[ANNEE_POINT, T_BUFFER]),
                               int(self.buffer[MOIS_POINT, T_BUFFER]),
                               int(self.buffer[JOUR_POINT, T_BUFFER]),
                               int(self.buffer[HEURE_POINT, T_BUFFER]))
        return date_mesure

    def Tendance(self):
        """
        Fourniture de l evolution des mesures :
            ecart entre la moyenne des 2 dernieres et des 2 prochaines heures
        Entree :
            aucune
        Sortie :
            tendance : valeur de l'ecart
        """
        moyenne_actu = (self.buffer[NON_FILTRE, T_BUFFER] +
                        self.buffer[NON_FILTRE, T_BUFFER-1]) / 2.0
        moyenne_futu = (self.b_pred_meil[0, 0] + self.b_pred_meil[0, 1]) / 2.0
        tendance = moyenne_futu - moyenne_actu
        return tendance

    def Historique(self):
        """
        Fourniture de l historique des mesures. La plus recente (T_BUFFER)
        correspond a la date fournie par Info_Date.
        Entree :
            aucune
        Sortie :
            histo : array de 0 (ancien) a T_BUFFER (actuel)
        """
        histo = zeros((T_BUFFER+1))
        histo = self.buffer[NON_FILTRE, 0:T_BUFFER+1]
        return histo

    def Historique_Filtre(self):
        """
        Fourniture de l historique des mesures filtrees. La plus recente
        (T_BUFFER) correspond a la date fournie par Info_Date.
        La plus recente est calculee avec egalement la premiere estimation.
        Entree :
            aucune
        Sortie :
            histo_filtre : array de [0] (ancien) a [T_BUFFER] (actuel)
        """
        histo_filtre = zeros((T_BUFFER+1))
        histo_filtre = self.buffer[FILTRE, 0:T_BUFFER+1]
        return histo_filtre

    def Ecart_Moyen(self, horizon=1):
        """
        Moyenne des ecarts absolus et relatif des 5 dernières predictions
        pour un horizon donne (1 par defaut).
        Renvoie -1 si les 5 dernieres valeurs sont nulles
        Entree :
            Horizon : horizon de prediction choisi (1 par defaut)
        Sortie :
            ecart_moyen : array avec [0] pour ecart absolu et [1] pour relatif
        """
        ecart_moyen = zeros((2))
        ecart_moyen[1] = -1.0
        valeurs = 0.0
        for i in range(5):
            ecart_moyen[0] += abs(self.buffer[NON_FILTRE, T_BUFFER-i] -
                                  self.b_pred_meil[horizon+i, horizon-1])
            valeurs += self.buffer[NON_FILTRE, T_BUFFER - i]
        if valeurs > 0.1:
            ecart_moyen[1] = ecart_moyen[0] / valeurs
        ecart_moyen[0] /= 5.0

        return ecart_moyen

    def Ecart_Moyen_Filtre(self, horizon=1):
        """
        Moyenne des ecarts absolus et relatif des 5 dernières predictions
        filtrees pour un horizon donne (1 par defaut).
        Renvoie -1 si les 5 dernieres valeurs sont nulles
        Entree :
            Horizon : horizon de prediction choisi (1 par defaut)
        Sortie :
            ecart_moyen : array avec [0] pour ecart absolu et [1] pour relatif
        """
        ecart_moyen_f = zeros((2))
        ecart_moyen_f[1] = -1.0
        valeurs = 0.0
        for i in range(5):
            ecart_moyen_f[0] += abs(self.buffer[FILTRE, T_BUFFER - i] -
                                    self.b_pred_filt[horizon + i, horizon - 1])
            valeurs += self.buffer[FILTRE, T_BUFFER-i]
        if valeurs > 0.1:
            ecart_moyen_f[1] = ecart_moyen_f[0] / valeurs
        ecart_moyen_f[0] /= 5.0

        return ecart_moyen_f

    def Ecart_Tendance(self):
        """
        Fourniture de la moyenne des écarts des 3 dernières tendances :
            ecart entre la tendance calculee sur les valeurs predites et
            la tendance calculee sur les valeurs reelles.
        Ecart fourni uniquement si l historique est de 24h
        Entree :
            aucune
        Sortie :
            ecart : moyenne des 3 ecarts
        """
        ecart = 0.0
        if self.buffer[NON_FILTRE, 0] > 0.1:
            for t in range(2, 5):
                prevu = (self.b_pred_meil[t, 0] +
                         self.b_pred_meil[t, 1]) / 2.0
                reel = (self.buffer[NON_FILTRE, T_BUFFER-t+1] +
                        self.buffer[NON_FILTRE, T_BUFFER-t+2]) / 2.0
                ecart += abs(prevu - reel)
            ecart /= 3.0
        return ecart

    def Debug_Pred(self):
        """
        Affichage des valeurs pour chaque pas de temps
        Sortie :
            écriture dans le fichier de debug FILE_DEBUG
        """
        for k in range(HORIZON):
            fichier = FILE_DEBUG + str(k) + '.csv'
            if (k == 0) or (k == 1 and DEBUG_PREDICTION2) or \
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
