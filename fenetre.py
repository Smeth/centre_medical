import sys
import time
import datetime
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, QIODevice,QSize, Qt, QCoreApplication
from PySide2.QtSql import QSqlTableModel, QSqlDatabase, QSqlError, QSqlQuery, QSqlQueryModel
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient, QIcon)

from PySide2 import QtCore, QtWidgets ,QtGui, QtSql

from Connexion import DataConnexion

class Application(QWidget):


    def __init__(self):
        
        super().__init__()
        
        '''initialisation des fenetres'''
        
        self.con = DataConnexion()



        #fenetre principal
        self.Ui_Acceuil = QUiLoader().load(QFile("./vues/Acceuil01.ui"))
        self.Ui_Acceuil.setWindowTitle(" Davina Gestion Clinique")
        self.Ui_Apropos = QUiLoader().load(QFile("./vues/aide.ui"))
        
        '''Appeler pour quitter l'application'''
        def quitter():
            self.msq = QtWidgets.QMessageBox()
            self.msq.setIcon(QtWidgets.QMessageBox.Warning)
            self.msq.setWindowTitle("Avertissement")
            self.msq.setInformativeText("Voulez vous Quitter l'application ?")
            self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            ret  = self.msq.exec_()
            
            if(ret == QMessageBox.Ok):

                QApplication.quit()

        def deconnection():

            self.msq = QtWidgets.QMessageBox()
            self.msq.setIcon(QtWidgets.QMessageBox.Warning)
            self.msq.setWindowTitle("Avertissement")
            self.msq.setInformativeText("Voulez vous Quitter l'application en vous d....?")
            self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            ret  = self.msq.exec_()
            
            if(ret == QMessageBox.Ok):
                
                self.__init__()
                
        icon = QIcon()
        #icon.addFile(u"res/icon/db_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Apropos.logo.setPixmap(QPixmap(u"./res/iconx250.png"))        

        self.Ui_Acceuil.actionQuitter.triggered.connect(quitter)
        self.Ui_Acceuil.deconnecter.triggered.connect(deconnection)
        self.Ui_Acceuil.actionA_propos.triggered.connect(self.Ui_Apropos.show)
        #QCoreApplication.exit(quitter)
        


        #fenetre de connexion   
        self.Ui_con = QUiLoader().load(QFile("./vues/connexion.ui"))
        self.Ui_con.setWindowTitle(" Authentification ")


        #fenetre gestion de la caisse 


        #Fenetre authentification
        self.Ui_con = QUiLoader().load(QFile("./vues/connexion.ui"))

        self.Ui_planifier_rdv = QUiLoader().load(QFile("./vues/planifier_rdv.ui"))
        
        
        '''Lancement de la fenetre d acceuil'''

        icon = QIcon()
        icon.addFile(u"res/icon/man.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actionPatient.setIcon(icon)
        
        icon.addFile(u"res/mod/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.setWindowIcon(icon)
    

        #Gestion des clicks fênetre principal
        self.Ui_Acceuil.actionPatient.triggered.connect(self.gestP)
        self.Ui_Acceuil.actionplaning.triggered.connect(self.gestRDV)
        self.Ui_Acceuil.actioncaisse.triggered.connect(self.gestCaisse)
        self.Ui_Acceuil.actionpara.triggered.connect(self.gest_Parametre)


        #Ajout des icon sur la barre de menue Gauche
        icon = QIcon()
        icon.addFile(u"res/ptt.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actionPatient.setIcon(icon)
        
        icon = QIcon()
        icon.addFile(u"res/calendrer_rdv.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actionplaning.setIcon(icon)

        icon = QIcon()
        icon.addFile(u"res/caisse.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actioncaisse.setIcon(icon)

        icon = QIcon()
        icon.addFile(u"res/pharma.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actionPharmacie.setIcon(icon)

        icon = QIcon()
        icon.addFile(u"res/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_Acceuil.actionpara.setIcon(icon)


        '''Gestion Des evenement'''

        
        #Gestion evenement module gestion patient
       



        '''Qmessage'''
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        '''demmarrage de la fenetre principale'''

        icon = QIcon()
        #icon.addFile(u"res/icon/db_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_con.logo.setPixmap(QPixmap(u"./res/iconx250.png"))

        self.Ui_con.show()

        self.Ui_con.B_connexion.clicked.connect(self.login)
        self.Ui_con.nom_u.returnPressed.connect(self.login)
        self.Ui_con.mdp_u.returnPressed.connect(self.login)
    
    def closeEvent(self, event):
        print(" Quitter l application")
    
    
    ##############""
    '''Gestion des patients, traitements, consultations'''


    def initialisation(self):
        self.gestCaisse()
        self.gestP()
        self.gestPharma()

    def gestP(self):

        self.Ui_gestP = QUiLoader().load(QFile("./vues/gestP.ui"))

        self.Ui_gestP.save_p.clicked.connect(self.Ajouter_Patient)
        self.Ui_gestP.btn_add.clicked.connect(self.Ajouter_Consultation)
        
        self.Ui_Acceuil.setCentralWidget(self.Ui_gestP)
        self.Afficher_Patient()

        '''icon Patient'''
        
        #formulaire
        icon = QIcon()
        icon.addFile(u"./res/ok.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.save_p.setIcon(icon)

        self.Ui_gestP.label_10.setPixmap(QPixmap(u"./res/icon/microscopex64.png"))

        self.Ui_gestP.label_13.setPixmap(QPixmap(u"./res/icon/cardiogramx64.png"))

        icon1 = QIcon()


        icon2 = QIcon()
        icon2.addFile(u"./res/ok.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_add.setIcon(icon2)
        self.Ui_gestP.btn_add.setIconSize(QSize(17, 24))

        icon4 = QIcon()

        icon4.addFile(u"./res/icon/rech.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_rech.setIcon(icon4)
        self.Ui_gestP.btn_rech.setIconSize(QSize(17, 12))

        icon5 = QIcon()
        icon6 = QIcon()
        icon6.addFile(u"./res/icon/037-place.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_ico.setIcon(icon6)
        
        icon6.addFile(u"./res/tel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_ico_tel.setIcon(icon6)

        icon6.addFile(u"./res/rdv.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.planif_rdv_p.setIcon(icon6)

        '''logo'''
        self.Ui_gestP.image_p.setPixmap(QPixmap(u"./res/iconx250.png"))
        self.Ui_gestP.image_p2.setPixmap(QPixmap(u"./res/iconx250.png"))
        self.Ui_gestP.image_p3.setPixmap(QPixmap(u"./res/iconx250.png"))



        icon5.addFile(u"./res/supp.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_supp_p.setIcon(icon5)

        icon5.addFile(u"./res/print.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.imprimer_p.setIcon(icon5)
        
        icon1.addFile(u"./res/icon/mod.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.btn_modifier_p.setIcon(icon1)
        self.Ui_gestP.btn_modifier_p.setIconSize(QSize(17, 24))

        '''icon consultation'''

        
        icon5.addFile(u"./res/supp.png", QSize(), QIcon.Normal, QIcon.Off)
        #self.Ui_gestP.btn_supp.setIcon(icon5)
        icon5.addFile(u"./res/icon/print.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestP.imprimer_2.setIcon(icon5)
        self.Ui_gestP.imprimer_c.setIcon(icon5)
        icon1.addFile(u"./res/icon/mod.png", QSize(), QIcon.Normal, QIcon.Off)
        #self.Ui_gestP.btn_modifier.setIcon(icon1)
        #self.Ui_gestP.btn_modifier.setIconSize(QSize(17, 24))
        #self.Ui_gestP.imprimer.setIcon(icon5)

        '''icon traitement '''
        
        self.list_patient()


        '''Detection de changement d'onglet puis affichage adéquat'''
        
        self.Ui_gestP.liste_patient.currentIndexChanged.connect(self.maj_id)

        
        if (self.Ui_gestP.cont_p.currentIndex() == 0):
            
            self.Afficher_Patient()
       
        elif(self.Ui_gestP.cont_p.currentIndex() == 1):
          
            self.list_patient()
            self.Afficher_Consultation()
            self.Afficher_Consultation_2()
     
        elif(self.Ui_gestP.cont_p.currentIndex() == 3):
            self.affiche_historique()

        self.affiche_historique()
        self.Ui_gestP.cont_p.currentChanged.connect(self.actualisation_data)
        
        '''Gestion evenement'''
        #self.Ui_gestP.vue_patient.
        self.Ui_gestP.planif_rdv_p.clicked.connect(self.planifierRdv)
        self.Ui_gestP.cont_p.currentChanged.connect(self.maj_id)
        self.Ui_gestP.cont_cons.currentChanged.connect(self.Afficher_Consultation)    
        self.Ui_gestP.rech_p.textEdited.connect(self.Recherche_Patient)
        self.Ui_gestP.btn_rech.clicked.connect(self.Recherche_Patient)
        self.Ui_gestP.btn_supp_p.clicked.connect(self.supp_Patient)
        self.Ui_gestP.btn_modifier_p.clicked.connect(self.Patient_info)
        
        '''Consultation'''
        
        self.Ui_gestP.mod_cons.clicked.connect(self.Consultation_info)
        self.Ui_gestP.supp_cons.clicked.connect(self.supp_Consultation)
        self.Ui_gestP.imprimer_c.clicked.connect(self.imprimer_d_cons)
        self.Ui_gestP.fiche_pat.clicked.connect(self.fiche_Patient)
        
        
    def actualisation_data(self):
     
        if (self.Ui_gestP.cont_p.currentIndex() == 0):
            
            self.Afficher_Patient()


        elif(self.Ui_gestP.cont_p.currentIndex() == 1):
          
            self.list_patient()
            self.Afficher_Consultation()
            self.Afficher_Consultation_2()

    def list_patient(self):
        
        query = QSqlQuery()

        query.exec_("select distinct patient.idPatient, patient.nomPatient, patient.prenomPatient from  patient, consultation where patient.idPatient in (select idPatient_c from consultation) group by idPatient")
        self.id_2 = {}
        self.Ui_gestP.liste_patient_t.clear()
        while query.next():

            self.Ui_gestP.liste_patient_t.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_2 [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))

        query.exec_("select distinct patient.idPatient, patient.nomPatient, patient.prenomPatient from  patient, consultation where patient.idPatient not in (select idPatient_c from consultation) group by idPatient")

        self.id_ = {}
        

        self.Ui_gestP.liste_patient.clear()
        while query.next(): 

            self.Ui_gestP.liste_patient.addItem(str(query.value(1))+" "+str(query.value(2)))
            #self.Ui_planifier_rdv.liste_patient.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_ [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))

    def  maj_id(self):
        pass


    ###########
    '''Les patients'''
    #Afficher Patient

    def Afficher_Patient(self):
        
        query = QSqlQuery()
        query.exec_("SELECT * FROM patient ")
        self.Ui_gestP.vue_patient.setRowCount(0)
        while query.next():  # Pour parcourir toute les données de la table personne avec comme indexe notre objet de
            # type QSqlQuery (query)

            self.Ui_gestP.vue_patient.insertRow(self.Ui_gestP.vue_patient.rowCount())
            #print("nbr = ", self.Ui_gestP.vue_patient.rowCount())
            row = self.Ui_gestP.vue_patient.rowCount() - 1

            self.Ui_gestP.vue_patient.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
            self.Ui_gestP.vue_patient.setItem(row, 1, QTableWidgetItem(str(query.value(8))))
            self.Ui_gestP.vue_patient.setItem(row, 2, QTableWidgetItem(str(query.value(1)))) 
            self.Ui_gestP.vue_patient.setItem(row, 3, QTableWidgetItem(str(query.value(2)))) 
            self.Ui_gestP.vue_patient.setItem(row, 4, QTableWidgetItem(str(query.value(3)))) 
            self.Ui_gestP.vue_patient.setItem(row, 5, QTableWidgetItem(str(query.value(4)))) 
            self.Ui_gestP.vue_patient.setItem(row, 6, QTableWidgetItem(str(query.value(6)))) 
            self.Ui_gestP.vue_patient.setItem(row, 7, QTableWidgetItem(str(query.value(7)))) 
    
    #Save Patient
    def Ajouter_Patient(self):
        
        query = QSqlQuery()
        query.prepare("INSERT INTO patient (nomPatient, prenomPatient, age, poids, adressePatient, telephone, sexe, dateAjout) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

        if(self.Ui_gestP.nom.text() == "" or self.Ui_gestP.prenom.text() == "" or self.Ui_gestP.age.value() == "" or self.Ui_gestP.poids.value() == "" or self.Ui_gestP.adresse.text() == "" or self.Ui_gestP.tel.text() == ""):        
        
            self.msg.setWindowTitle("Champ(s) vide(s)")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Veuillez remplir tous les champs ")
            
            self.msg.exec_()
            
        
        else:

            query.bindValue(0, str(self.Ui_gestP.nom.text()))
            query.bindValue(1, str(self.Ui_gestP.prenom.text()));
            query.bindValue(2, str(self.Ui_gestP.age.value()))
            query.bindValue(3, str(self.Ui_gestP.poids.value()))
            query.bindValue(4, str(self.Ui_gestP.adresse.text()));
            query.bindValue(5, str(self.Ui_gestP.tel.text()))
            query.bindValue(7, str(datetime.date.today()))

            if (self.Ui_gestP.btn_M.isChecked()):
                query.bindValue(6, str('M'))
            elif(self.Ui_gestP.btn_F.isChecked()):
                 query.bindValue(6, str('F'))

            v = query.exec_()
            
            if(v and self.Ui_gestP.nom.text() != "" and self.Ui_gestP.prenom.text() != "" and self.Ui_gestP.age.value() != "" and self.Ui_gestP.adresse.text() != ""  and self.Ui_gestP.tel.text() != ""  ):
               
                self.msg.setText("Patient Ajouter")
                self.msg.exec_()
                self.Afficher_Patient()
                '''
                self.Ui_gestP.nom.clear()
                self.Ui_gestP.prenom.clear()
                self.Ui_gestP.age.clear()
                '''
                
            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Patient non Ajouter"+str(query.lastError()))
                self.msg.exec_()
            
    def Recherche_Patient(self):

       
        con = DataConnexion()
        
        query = QSqlQuery()
        query.exec_("SELECT * FROM patient where nomPatient like \'%"+str(self.Ui_gestP.rech_p.text())+"%\' or prenomPatient like \'%"+str(self.Ui_gestP.rech_p.text())+"%\' ")
        
        self.Ui_gestP.vue_patient.setRowCount(0)

        while query.next():

            self.Ui_gestP.vue_patient.insertRow(self.Ui_gestP.vue_patient.rowCount())
            #print("nbr = ", self.Ui_gestP.vue_patient.rowCount())
            row = self.Ui_gestP.vue_patient.rowCount() - 1


            self.Ui_gestP.vue_patient.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
            self.Ui_gestP.vue_patient.setItem(row, 2, QTableWidgetItem(str(query.value(1)))) 
            self.Ui_gestP.vue_patient.setItem(row, 3, QTableWidgetItem(str(query.value(2)))) 
            self.Ui_gestP.vue_patient.setItem(row, 4, QTableWidgetItem(str(query.value(3)))) 
            self.Ui_gestP.vue_patient.setItem(row, 5, QTableWidgetItem(str(query.value(4)))) 
            self.Ui_gestP.vue_patient.setItem(row, 6, QTableWidgetItem(str(query.value(6)))) 
            self.Ui_gestP.vue_patient.setItem(row, 7, QTableWidgetItem(str(query.value(7))))
    
    def supp_Patient(self):

        self.msq = QtWidgets.QMessageBox()
        self.msq.setIcon(QtWidgets.QMessageBox.Warning)
        self.msq.setWindowTitle("Avertissement")
        self.msq.setInformativeText("Voulez vous vraiment supprimer ce patient ?")
        self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret  = self.msq.exec_()

        if(ret == QMessageBox.Ok):

            l = self.Ui_gestP.vue_patient.currentRow()
            #print( 'id === = ', str(self.Ui_gestP.vue_patient.item(l, 0).text()))
            query = QSqlQuery()

            query.prepare("DELETE from  patient where idPatient = ?")

            query.bindValue(0, int(str(self.Ui_gestP.vue_patient.item(l, 0).text())))
            
            v = query.exec_()

            #print("il contient ",v, "erreur", query.lastError())
            
            if(v):
                self.msg.setText("Patient supprimer")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
                self.Afficher_Patient()

            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Ecehc de suppression "+str(query.lastError()))
                self.msg.exec_()

    def Patient_info(self):
        #self.getcell()
        self.Ui_mod_Patient = QUiLoader().load(QFile("./vues/mod_patient.ui"))
        
        '''recupere la ligne actuellement selectionné'''
        l = self.Ui_gestP.vue_patient.currentRow()
        #recupere l id de la ligne
        id=int(str(self.Ui_gestP.vue_patient.item(l, 0).text()))
        query = QSqlQuery()
        query.exec_("SELECT * FROM patient where idPatient = "+str(id))

        while query.next():
            
            self.Ui_mod_Patient.nom.setText(str(query.value(1)))
            self.Ui_mod_Patient.prenom.setText(str(query.value(2)))
            self.Ui_mod_Patient.age.setValue( int(query.value(3)))
            self.Ui_mod_Patient.poids.setValue(float(query.value(4)))
            self.Ui_mod_Patient.adresse.setText(str(query.value(5)))
            self.Ui_mod_Patient.tel.setText(str(query.value(6)))

        self.Ui_mod_Patient.show()
        self.Ui_mod_Patient.save_p.clicked.connect(self.mod_Patient)

    def mod_Patient(self):

        l = self.Ui_gestP.vue_patient.currentRow()
        #recupere l id de la ligne
        id=int(str(self.Ui_gestP.vue_patient.item(l, 0).text()))
        
        query = QSqlQuery()
        query.prepare("""UPDATE patient 
                                SET nomPatient = ?, prenomPatient=?, 
                                age=?, poids=?, adressePatient=?, telephone=?, sexe = ?
                                    where idPatient = ? """)
                
        query.bindValue(0, str(self.Ui_mod_Patient.nom.text()))
        query.bindValue(1, str(self.Ui_mod_Patient.prenom.text()));
        query.bindValue(2, int(self.Ui_mod_Patient.age.value()))
        query.bindValue(3, float(self.Ui_mod_Patient.poids.value()))
        query.bindValue(4, str(self.Ui_mod_Patient.adresse.text()));
        query.bindValue(5, str(self.Ui_mod_Patient.tel.text()))

        if  (self.Ui_mod_Patient.btn_M.isChecked()):
            query.bindValue(6, str('M'))
        elif(self.Ui_mod_Patient.btn_F.isChecked()):
            query.bindValue(6, str('F'))

        query.bindValue(7, int(id))

        v = query.exec_()
        
        if(v and self.Ui_mod_Patient.nom.text() != "" and self.Ui_mod_Patient.prenom.text() != "" and self.Ui_mod_Patient.age.value() != "" and self.Ui_mod_Patient.adresse.text() != ""  and self.Ui_mod_Patient.tel.text() != ""  ):
            
            self.msg.setText("Patient Modifier")
            self.msg.exec_()
            self.Afficher_Patient()
            self.Ui_mod_Patient.close()
            
        else:
            self.msg.setWindowTitle("Echec !!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Patient non Modifier"+str(query.lastError()))
            self.msg.exec_()

    ###########
    ''' Les Traitements ........'''
   
    def Afficher_Traitement(self):
        
        query = QSqlQuery()
        query.exec_("SELECT * FROM traitement")

        cpt  = 0
        while query.next():

            self.Ui_gestP.vue_traitement.insertRow(self.Ui_gestP.vue_patient.rowCount())
            
            row = self.Ui_gestP.vue_traitement.rowCount() - 1

            self.Ui_gestP.vue_traitement.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
            self.Ui_gestP.vue_traitement.setItem(row, 1, QTableWidgetItem(query.value(1))) 
            self.Ui_gestP.vue_traitement.setItem(row, 2, QTableWidgetItem(query.value(2))) 
            self.Ui_gestP.vue_traitement.setItem(row, 3, QTableWidgetItem(query.value(3))) 
            cpt = cpt +1

        print ("il y a ", cpt)

    def Ajouter_Traitement(self):
        
        self.list_patient()
        query = QSqlQuery()
        query.prepare("INSERT INTO traitement (idPatient, idDoc, Traitement) VALUES (?, ?, ?)")


        query.bindValue(0, int(str(self.id_ [self.Ui_gestP.liste_patient_2.currentText()])))
        query.bindValue(1, int(1))
        query.bindValue(2, str(self.Ui_gestP.traitement_val.toPlainText()))
        v = query.exec_()
        
        if(v):
            self.msg.setText("Patient Ajouter")
            self.msg.exec_()
            self.Afficher_Patient()

            
        else:
            self.msg.setWindowTitle("Echec !!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Patient non Ajouter"+str(query.lastError()))
            self.msg.exec_()

    def Recherche_trait(self):
        pass

    def supp_Traitement(self):
    
        self.msq = QtWidgets.QMessageBox()
        self.msq.setIcon(QtWidgets.QMessageBox.Warning)
        self.msq.setWindowTitle("Avertissement")
        self.msq.setInformativeText("Voulez vous vraiment supprimer ce patient ?")
        self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        self.msq.exec_()
        
        if(self.msq.clickedButton() == 0x00004000):

            l = self.Ui_gestP.vue_traitement.currentRow()
            #c = self.Ui_gestRDV.vue_rdv.currentColumn()
            print( 'id === = ', str(self.Ui_gestP.vue_traitement.item(l, 0).text()))
            query = QSqlQuery()

            query.prepare("DELETE from  patient where idPatient = ?")

            query.bindValue(0, int(str(self.Ui_gestP.vue_traitement.item(l, 0).text())))
            
            v = query.exec_()

            #print("il contient ",v, "erreur", query.lastError())
            
            if(v):
                self.msg.setText("Patient supprimer")
                self.msg.exec_()
                self.Afficher_Patient()

            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Ecehc de suppression "+str(query.lastError()))
                self.msg.exec_()

    ##########
    ''' Les consultations '''

    def list_docteur(self):

        query = QSqlQuery()

        query.exec_("select distinct * from  docteur")
        self.id_doc = {}
        self.Ui_gestP.liste_docteur.clear()
        
        while query.next():

            self.Ui_gestP.liste_docteur.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_doc [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))

    def Afficher_Consultation(self):

        self.list_patient()
        self.list_docteur()
        if (self.Ui_gestP.cont_cons.currentIndex() == 0):

            query = QSqlQuery()
            query.exec_("""select * from  patient 
                                        where idPatient not in 
                                            (select idPatient_c from consultation) group by idPatient """)

            print("index : ", self.Ui_gestP.cont_cons.currentIndex())

            self.Ui_gestP.vue_cons_no.setRowCount(0)
            while query.next():  

                self.Ui_gestP.vue_cons_no.insertRow(self.Ui_gestP.vue_cons_no.rowCount())
                row = self.Ui_gestP.vue_cons_no.rowCount() - 1


                self.Ui_gestP.vue_cons_no.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
                self.Ui_gestP.vue_cons_no.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
                self.Ui_gestP.vue_cons_no.setItem(row, 2, QTableWidgetItem(str(query.value(2)))) 
                self.Ui_gestP.vue_cons_no.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
                self.Ui_gestP.vue_cons_no.setItem(row, 4, QTableWidgetItem(str(query.value(4))))
                self.Ui_gestP.vue_cons_no.setItem(row, 5, QTableWidgetItem(str(query.value(5))))
                self.Ui_gestP.vue_cons_no.setItem(row, 6, QTableWidgetItem(str(query.value(6))))
                self.Ui_gestP.vue_cons_no.setItem(row, 7, QTableWidgetItem(str(query.value(7))))
                self.Ui_gestP.vue_cons_no.setItem(row, 8, QTableWidgetItem(str(query.value(8))))



        elif(self.Ui_gestP.cont_cons.currentIndex() == 1) : 
            self.Afficher_Consultation_2()

    def Afficher_Consultation_2(self):
            
            self.list_docteur()
            
            print("index : ", self.Ui_gestP.cont_cons.currentIndex())
            query = QSqlQuery()
            #select patient.nomPatient, patient.idPatient from  patient, consultation where idPatient  in (select idPatient from consultation)
            query.exec_("select consultation.idConsultation, patient.idPatient,  patient.nomPatient, patient.prenomPatient, patient.age,  patient.sexe, consultation.symptome, consultation.examen, consultation.dateConsultation from  patient, consultation where patient.idPatient = consultation.idPatient_c ")

            self.Ui_gestP.vue_cons_2.setRowCount(0)
            
            while query.next():  # Pour parcourir toute les données de la table personne avec comme indexe notre objet de
                # type QSqlQuery (query)

                self.Ui_gestP.vue_cons_2.insertRow(self.Ui_gestP.vue_cons_2.rowCount())
                #print("nbr = ", self.Ui_gestP.vue_patient.rowCount())
                row = self.Ui_gestP.vue_cons_2.rowCount() - 1

                self.Ui_gestP.vue_cons_2.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
                self.Ui_gestP.vue_cons_2.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
                self.Ui_gestP.vue_cons_2.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
                self.Ui_gestP.vue_cons_2.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
                self.Ui_gestP.vue_cons_2.setItem(row, 4, QTableWidgetItem(str(query.value(4))))
                self.Ui_gestP.vue_cons_2.setItem(row, 5, QTableWidgetItem(str(query.value(5))))   
                self.Ui_gestP.vue_cons_2.setItem(row, 6, QTableWidgetItem(str(query.value(6))))
                self.Ui_gestP.vue_cons_2.setItem(row, 7, QTableWidgetItem(str(query.value(7))))
                self.Ui_gestP.vue_cons_2.setItem(row, 8, QTableWidgetItem(str(query.value(8))))   
   
    def Ajouter_Consultation(self):
        
        self.list_patient()

        if(self.Ui_gestP.symptome.toPlainText() == "" or self.Ui_gestP.liste_patient.currentText() ==""  ):
    
            self.msg.setWindowTitle("Champ(s) vide(s)")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Veuillez Ajoutez un Symptome ou selectionné un patient ")
            self.msg.exec_()
        
        else:

            query = QSqlQuery()
            query.prepare("INSERT INTO consultation (idPatient_c, idDoc, dateConsultation, Symptome, Prix_Consultation, examen) VALUES ( ?,?, ?, ?, ?, ?)")


            query.bindValue(0, int(str(self.id_ [self.Ui_gestP.liste_patient.currentText()])))
            query.bindValue(1, str('1'))
            query.bindValue(2, str(datetime.date.today()))
            query.bindValue(3, str(self.Ui_gestP.symptome.toPlainText()))
            query.bindValue(4, str('5000'))
            query.bindValue(5, str(self.Ui_gestP.examen.toPlainText()))
            
            print ("mr : ",  str(self.id_ [self.Ui_gestP.liste_patient.currentText()]))
            v = query.exec_()

            #print("il contient ",v, "erreur", query.lastError())
            
            if(v and self.Ui_gestP.symptome.toPlainText() != ""):
                self.msg.setText("Consultation Ajouter")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
                self.Ui_gestP.vue_cons_no.clearContents()
                self.Ui_gestP.vue_cons_no.update()
                
                self.Afficher_Consultation()
                self.Ui_gestP.symptome.clear()

            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Symptome non Ajouter"+str(query.lastError()))
                self.msg.exec_()

    def recherche_Consultation(self):
        pass

    def Consultation_info(self):
            #self.getcell()
        self.Ui_mod_cons = QUiLoader().load(QFile("./vues/mod_cons.ui"))
        
        '''recupere la ligne actuellement selectionné'''
        l = self.Ui_gestP.vue_cons_2.currentRow()
        #recupere l id de la ligne
        id=int(str(self.Ui_gestP.vue_cons_2.item(l, 1).text()))
        query = QSqlQuery()
        query.exec_("""select consultation.idConsultation, patient.idPatient,  patient.nomPatient, patient.prenomPatient, consultation.symptome, consultation.examen, consultation.dateConsultation 
                            from  patient, consultation 
                                where consultation.idPatient_c  = """+str(id)+""" And patient.idPatient =  """+str(id))

        while query.next():
           self.Ui_mod_cons.id.setText(str(query.value(1))+" - "+ str(query.value(2))+" - " + str(query.value(3)))
           self.Ui_mod_cons.consultation.setPlainText(str(query.value(4)))
           self.Ui_mod_cons.Examen.setPlainText(str(query.value(5)))
           
        query = QSqlQuery()

        query.exec_("select distinct * from  docteur")
        self.id_doc = {}
        self.Ui_mod_cons.liste_docteur.clear()
        
        while query.next():

            self.Ui_mod_cons.liste_docteur.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_doc [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))
        
        self.Ui_mod_cons.liste_docteur.setCurrentText(str(self.Ui_gestP.vue_cons_2.item(l, 4).text()))
        self.Ui_mod_cons.show()
        self.Ui_mod_cons.save_c.clicked.connect(self.mod_consultation)

    def mod_consultation(self):
        pass
  
    def supp_Consultation(self):
        
        self.msq = QtWidgets.QMessageBox()
        self.msq.setIcon(QtWidgets.QMessageBox.Warning)
        self.msq.setWindowTitle("Avertissement")
        self.msq.setInformativeText("Voulez vous vraiment supprimer cette consultation ?")
        self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret=self.msq.exec_()

        if(ret == QMessageBox.Ok):

            l = self.Ui_gestP.vue_cons_2.currentRow()
           
            query = QSqlQuery()

            query.prepare("DELETE from  consultation where idConsultation = ? ")

            query.bindValue(0, int(str(self.Ui_gestP.vue_cons_2.item(l, 0).text())))
            
            v = query.exec_()

            #print("il contient ",v, "erreur", query.lastError())
            
            if(v):
                self.msg.setText("Patient supprimer")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
                self.Afficher_Consultation_2()

            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Echec de suppression "+str(query.lastError()))
                self.msg.exec_()

    def fiche_Patient(self):
           
        self.Ui_Fiche_Patient = QUiLoader().load(QFile("./vues/fiche_patient.ui"))
        
        l = self.Ui_gestP.vue_cons_2.currentRow()
        '''recupere l id de la ligne'''
        id=int(str(self.Ui_gestP.vue_cons_2.item(l, 1).text()))

        query = QSqlQuery()
        
        query.exec_("SELECT * FROM patient where idPatient = "+str(id))

        while query.next():
            
            self.Ui_Fiche_Patient.nom.setText(str(query.value(1)))
            self.Ui_Fiche_Patient.prenom.setText(str(query.value(2)))
            self.Ui_Fiche_Patient.sexe.setText( str(query.value(7)))
            self.Ui_Fiche_Patient.age.setText( str(query.value(3)))
            self.Ui_Fiche_Patient.poids.setText(str(query.value(4)))
            self.Ui_Fiche_Patient.add.setText(str(query.value(5)))
            self.Ui_Fiche_Patient.tel.setText(str(query.value(6)))
        
        
        query = QSqlQuery()
        query.exec_("""select consultation.idConsultation, 
                            consultation.dateConsultation, 
                                consultation.symptome, consultation.examen 
                                    from consultation where idPatient_c = """+str(id))
        
        while query.next():
                
                self.Ui_Fiche_Patient.vue.insertRow(self.Ui_Fiche_Patient.vue.rowCount())
                #print("nbr = ", self.Ui_gestP.vue_patient.rowCount())
                row = self.Ui_Fiche_Patient.vue.rowCount() - 1

                self.Ui_Fiche_Patient.vue.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
                self.Ui_Fiche_Patient.vue.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
                self.Ui_Fiche_Patient.vue.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
                self.Ui_Fiche_Patient.vue.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
                self.Ui_Fiche_Patient.vue.setItem(row, 4, QTableWidgetItem(str(query.value(4))))
                self.Ui_Fiche_Patient.vue.setItem(row, 5, QTableWidgetItem(str(query.value(5))))   
                self.Ui_Fiche_Patient.vue.setItem(row, 6, QTableWidgetItem(str(query.value(6))))
                self.Ui_Fiche_Patient.vue.setItem(row, 7, QTableWidgetItem(str(query.value(7))))
                self.Ui_Fiche_Patient.vue.setItem(row, 8, QTableWidgetItem(str(query.value(8)))) 
        
        self.Ui_Fiche_Patient.show()
        
    def imprimer_d_cons(self):
        pass

    ###########
    '''Historique'''

    def affiche_historique(self):
        
        query = QSqlQuery()
        query.exec_("SELECT * FROM patient ")
        self.Ui_gestP.vue_historique.setRowCount(0)
        while query.next():  # Pour parcourir toute les données de la table personne avec comme indexe notre objet de
            # type QSqlQuery (query)

            self.Ui_gestP.vue_historique.insertRow(self.Ui_gestP.vue_historique.rowCount())
            #print("nbr = ", self.Ui_gestP.vue_historique.rowCount())
            row = self.Ui_gestP.vue_historique.rowCount() - 1

            self.Ui_gestP.vue_historique.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
            self.Ui_gestP.vue_historique.setItem(row, 1, QTableWidgetItem(str(query.value(8))))
            self.Ui_gestP.vue_historique.setItem(row, 2, QTableWidgetItem(str(query.value(1)))) 
            self.Ui_gestP.vue_historique.setItem(row, 3, QTableWidgetItem(str(query.value(2)))) 
            self.Ui_gestP.vue_historique.setItem(row, 4, QTableWidgetItem(str(query.value(3)))) 
            self.Ui_gestP.vue_historique.setItem(row, 5, QTableWidgetItem(str(query.value(4)))) 
            self.Ui_gestP.vue_historique.setItem(row, 6, QTableWidgetItem(str(query.value(6)))) 
            self.Ui_gestP.vue_historique.setItem(row, 7, QTableWidgetItem(str(query.value(7)))) 
    
    def affiche_inventaire(self):
        pass

    def supp_historique(self):
        pass

    def imp_historique(self):
        pass

    ###########
    '''Gestion des RDV'''

    def gestRDV(self):

        self.Ui_gestRDV = QUiLoader().load(QFile("./vues/rdv.ui"))  
                #fenetre planifier R.D.V
        self.Ui_planifier_rdv = QUiLoader().load(QFile("./vues/planifier_rdv.ui"))
        self.Ui_planifier_rdv.setWindowTitle(" Planifier un rdv")

        #Gestion des evenements
        self.Ui_gestRDV.planif_rdv.clicked.connect(self.planifierRdv)
        self.Ui_gestRDV.supp_rdv.clicked.connect(self.supp_rdv )

        self.Ui_gestRDV.vue_rdv.cellClicked.connect(self.getcell)
        self.Ui_gestRDV.vue_rdv.itemActivated.connect(self.getcell)
        self.Ui_Acceuil.setCentralWidget(self.Ui_gestRDV)

        self.Ui_gestRDV.calendrier_rdv.setGridVisible(True)
        
        '''ajout des icon '''

        icon = QIcon()
        icon.addFile(u"./res/refresh.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.act_rdv.setIcon(icon)

        icon.addFile(u"./res/supp.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.supp_rdv.setIcon(icon)

        icon.addFile(u"./res/print.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.imp_rdv.setIcon(icon)

        icon.addFile(u"./res/anul.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.anu_rdv.setIcon(icon)

        icon.addFile(u"./res/rdv.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.planif_rdv.setIcon(icon)
        
        icon.addFile(u"./res/icon/modif.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestRDV.mod_rdv.setIcon(icon)

        self.Ui_gestRDV.image_rdv.setPixmap(QPixmap(u"./res/iconx250.png"))
        
        #print("La date sélectionné est : ", str(self.Ui_gestRDV.calendrier_rdv.selectedDate()))
       
        self.Afficher_RDV()
   
    def list_patient_rdv(self):
        
        query = QSqlQuery()
        query.exec_("select patient.idPatient, patient.nomPatient, patient.prenomPatient from  patient ")

        self.id_ = {}
        

        self.Ui_planifier_rdv.liste_patient.clear()
     
        while query.next(): 

           
            self.Ui_planifier_rdv.liste_patient.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_ [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))

        print(self.id_)
    
    def getcell(self):

        nbcol = self.Ui_gestRDV.vue_rdv.columnCount()


        l = self.Ui_gestRDV.vue_rdv.currentRow()
        c = self.Ui_gestRDV.vue_rdv.currentColumn()
        print( 'lll', str(self.Ui_gestRDV.vue_rdv.item(l, 0).text()))
        cpt= 0
        tc = self.Ui_gestRDV.vue_rdv.columnCount()
      
        lg = []

        '''
        while cpt < tc :
            print ("l = ", l, "tc = ", tc, "cpt = ", cpt)
            lg.append(str(self.Ui_gestRDV.vue_rdv.itemAt(l, cpt ).text()))	
            cpt = cpt+1
        '''
        #print("la ligne = ", lg)
        #print("elle contient ", str(self.Ui_gestRDV.vue_rdv.currentItem().text()))

        #print ("la ligne contient ", list(self.Ui_gestRDV.vue_rdv.selectedItems()) )

    def mod_rdv(self):
        pass

    def supp_rdv(self):
        
        self.msq = QtWidgets.QMessageBox()
        self.msq.setIcon(QtWidgets.QMessageBox.Warning)
        self.msq.setWindowTitle("Avertissement")
        self.msq.setInformativeText("Voulez vous vraiment supprimer ce R.D.V ?")
        self.msq.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        ret  = self.msq.exec_()

        if(ret == QMessageBox.Ok):

            l = self.Ui_gestRDV.vue_rdv.currentRow()
            #c = self.Ui_gestRDV.vue_rdv.currentColumn()
            print( 'id === = ', str(self.Ui_gestRDV.vue_rdv.item(l, 0).text()))
            query = QSqlQuery()

            query.prepare("DELETE from  rdv where id = ?")

            query.bindValue(0, int(str(self.Ui_gestRDV.vue_rdv.item(l, 0).text())))
            
            v = query.exec_()

            #print("il contient ",v, "erreur", query.lastError())
            
            if(v):
                self.msg.setText("Rendez-Vous supprimer")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
                self.Ui_planifier_rdv.close()
                self.Afficher_RDV()

            else:
                self.msg.setWindowTitle("Echec !!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                self.msg.setText("Ecehc de suppression "+str(query.lastError()))
                self.msg.exec_()

    def Afficher_RDV(self):
        
        query = QSqlQuery()
        query.exec_("SELECT distinct rdv.id, patient.nomPatient, patient.prenomPatient, patient.sexe, rdv.motif, rdv.dateRdv, rdv.hrs FROM rdv, patient where patient.idPatient = rdv.idPatient ")
        cpt  = 0

        self.Ui_gestRDV.vue_rdv.setRowCount(0)
        while query.next(): 

            self.Ui_gestRDV.vue_rdv.insertRow(self.Ui_gestRDV.vue_rdv.rowCount())

            row = self.Ui_gestRDV.vue_rdv.rowCount() - 1

            self.Ui_gestRDV.vue_rdv.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
            self.Ui_gestRDV.vue_rdv.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
            self.Ui_gestRDV.vue_rdv.setItem(row, 2, QTableWidgetItem(str(query.value(2)))) 
            self.Ui_gestRDV.vue_rdv.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.Ui_gestRDV.vue_rdv.setItem(row, 4, QTableWidgetItem(str(query.value(4))))
            self.Ui_gestRDV.vue_rdv.setItem(row, 5, QTableWidgetItem(str(query.value(5))))
            self.Ui_gestRDV.vue_rdv.setItem(row, 6, QTableWidgetItem(str(query.value(6))))
            cpt = cpt +1
    
    def planifierRdv(self):
        #self.Ui_planifier_rdv.liste_patient.currentIndexChanged.connect(self.maj_id)
        self.Ui_planifier_rdv.show()
        self.list_patient_rdv()
        
        self.Ui_planifier_rdv.planifier_rdv.clicked.connect(self.Ajouter_Rdv)

    def Ajouter_Rdv(self):
        
        #self.list_patient_rdv()
        
        #print("Le dict des rdv contient ", self.id_)
        #print ("l id du text courant est", self.Ui_planifier_rdv.liste_patient.currentText()), " = ", int(str(self.id_ [self.Ui_planifier_rdv.liste_patient.currentText()]))
        query = QSqlQuery()

        query.prepare("INSERT INTO rdv (idPatient, idDocteur, dateRdv, motif, hrs) VALUES ( ?, ?, ?, ?, ?)")

        query.bindValue(0, int(str(self.id_ [self.Ui_planifier_rdv.liste_patient.currentText()])))
        query.bindValue(1, str('1'))
        query.bindValue(2, str(self.Ui_planifier_rdv.date_rdv.date().toString("dd-MM-yyyy")))
        query.bindValue(3, str(self.Ui_planifier_rdv.motif.text()))
        query.bindValue(4, str(self.Ui_planifier_rdv.rdv_t.time().toString()))

       
        
        v = query.exec_()

        #print("il contient ",v, "erreur", query.lastError())
        
        if(v):
            self.msg.setText("Rendez-Vous Planifier")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            self.Ui_planifier_rdv.close()
            self.Afficher_RDV()

        else:
            self.msg.setWindowTitle("Echec !!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("RDV non planifier"+str(query.lastError()))
            self.msg.exec_()
        
    def rech_RDV(self):
        pass    
  

    ###############
    '''Gestion de la caisse'''        

    def gestCaisse(self):

        self.Ui_decaissement = QUiLoader().load(QFile("./vues/decaissment.ui"))
       
        self.Ui_gestCaisse = QUiLoader().load(QFile("./vues/Caisse.ui"))
        self.Ui_Acceuil.setCentralWidget(self.Ui_gestCaisse)
        self.Ui_gestCaisse.setWindowTitle(" Caisse")
        self.Ui_gestCaisse.date_01.setDisplayFormat(("yyyy-MM-dd"))
        self.Ui_gestCaisse.show()
        
        self.Ui_gestCaisse.calendrier.selectionChanged.connect(self.Affiche_Date)
        self.Ui_gestCaisse.date_01.setDisplayFormat(("yyyy-MM-dd"))
        #self.Ui_gestCaisse.label_total.setText(str(self.Ui_gestCaisse.date_01.date().toString("dd / MM /yyyy")))
        self.Ui_gestCaisse.label_date.setText( " Liste des opérations du  : "+str(self.Ui_gestCaisse.calendrier.selectedDate().toString("dd / MM /yyyy")))
        
        #Ajout des icon 
        icon = QIcon()
        #icon.addFile(u"res/icon/operation.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestCaisse.logo_caisse.setPixmap(QPixmap(u"./res/iconx250.png"))
       

        icon.addFile(u"./res/afficher.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestCaisse.afficher.setIcon(icon)
        icon.addFile(u"./res/refresh.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestCaisse.Actualiser.setIcon(icon)
        icon.addFile(u"./res/print.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Ui_gestCaisse.imprimer_caisse.setIcon(icon)

   

        self.affiche_dec_caisse()
        self.affiche_caisse()


       
        self.Ui_gestCaisse.calendrier.selectionChanged.connect(self.affiche_caisse)
        self.Ui_gestCaisse.cont.currentChanged.connect(self.affiche_caisse)

        self.Ui_gestCaisse.btn_imp_caisse.clicked.connect(self.imprimer_caisse)
        self.Ui_gestCaisse.afficher.clicked.connect(self.Affiche_at)

        #self.Ui_gestCaisse.btn_decaiss.clicked.connect(self.OperationCaisse)

    def affiche_caisse(self):       

        if (self.Ui_gestCaisse.cont.currentIndex() == 0):
            query = QSqlQuery()

            
            montant = "SELECT SUM(Prix_Consultation) from consultation where dateConsultation = "+"'"+ str(self.Ui_gestCaisse.calendrier.selectedDate().toString("yyyy-MM-dd"))+"'"
            
            query.exec_(montant)

            while query.next():
                

                self.Ui_gestCaisse.label_total.setText("Total : "+ str(query.value(0))+" FCFA")
                print(' la caisse contient : ', str(query.value(0)))




            req = "SELECT * FROM consultation where dateConsultation = "+" '"+ str(self.Ui_gestCaisse.calendrier.selectedDate().toString("yyyy-MM-dd"))+"'"
               
            query.exec_(req)
                

            self.Ui_gestCaisse.vue_caisse.setRowCount(0)
            

            while query.next():


                self.Ui_gestCaisse.vue_caisse.insertRow(self.Ui_gestCaisse.vue_caisse.rowCount())
                
                
                row = self.Ui_gestCaisse.vue_caisse.rowCount() - 1

                self.Ui_gestCaisse.vue_caisse.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
                self.Ui_gestCaisse.vue_caisse.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 2, QTableWidgetItem(str(query.value(2)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 3, QTableWidgetItem(str(query.value(3)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 4, QTableWidgetItem(str(query.value(4)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 5, QTableWidgetItem(str(query.value(5))))      
 

            
        else : 
            self.affiche_dec_caisse()
   
    def Affiche_Date(self):
        #self.Ui_gestCaisse.label_date.setText("")
        self.Ui_gestCaisse.label_date.setText( " Liste des opérations du  : "+str(self.Ui_gestCaisse.calendrier.selectedDate().toString(" dd / MM / yyyy ")))

    def Affiche_at(self):

        query = QSqlQuery()

        if(self.Ui_gestCaisse.cont.currentIndex() == 0):
            
            
            
            montant = "SELECT SUM(Prix_Consultation) from consultation where dateConsultation between "+" '"+ str(self.Ui_gestCaisse.date_01.date().toString("yyyy-MM-dd"))+"' and '" +str(self.Ui_gestCaisse.date_02.date().toString("yyyy-MM-dd")) +"'"
            
            query.exec_(montant)

            while query.next():
                

                self.Ui_gestCaisse.label_total.setText("Total : "+ str(query.value(0))+" FCFA")
                print(' la caisse contient : ', str(query.value(0)))




            req = "SELECT * FROM consultation where dateConsultation between "+" '"+ str(self.Ui_gestCaisse.date_01.date().toString("yyyy-MM-dd"))+"' and '" +str(self.Ui_gestCaisse.date_02.date().toString("yyyy-MM-dd")) +"'"
               
            query.exec_(req)
            
            print(req)

            self.Ui_gestCaisse.vue_caisse.setRowCount(0)
            

            while query.next():


                self.Ui_gestCaisse.vue_caisse.insertRow(self.Ui_gestCaisse.vue_caisse.rowCount())
                
                
                row = self.Ui_gestCaisse.vue_caisse.rowCount() - 1

                self.Ui_gestCaisse.vue_caisse.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # colonne 0 (Id)
                self.Ui_gestCaisse.vue_caisse.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 2, QTableWidgetItem(str(query.value(2)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 3, QTableWidgetItem(str(query.value(3)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 4, QTableWidgetItem(str(query.value(4)))) 
                self.Ui_gestCaisse.vue_caisse.setItem(row, 5, QTableWidgetItem(str(query.value(5))))      
 

            
        else : 
            self.affiche_dec_caisse()

    #affiche decaissement
    def affiche_dec_caisse(self):       
        
        
        query = QSqlQuery()

        req = "SELECT * FROM Decaissement where Date = "+" '"+ str(self.Ui_gestCaisse.calendrier.selectedDate().toString("yyyy-MM-dd"))+"'"
    
     
        query.exec_(req)
            
        self.Ui_gestCaisse.vue_dec_caisse.setRowCount(0)
        
        while query.next():

            self.Ui_gestCaisse.vue_dec_caisse.insertRow(self.Ui_gestCaisse.vue_dec_caisse.rowCount())

            row = self.Ui_gestCaisse.vue_dec_caisse.rowCount() - 1

            self.Ui_gestCaisse.vue_dec_caisse.setItem(row, 0, QTableWidgetItem(str(query.value(0)))) 
            self.Ui_gestCaisse.vue_dec_caisse.setItem(row, 1, QTableWidgetItem(str(query.value(1)))) 
            self.Ui_gestCaisse.vue_dec_caisse.setItem(row, 2, QTableWidgetItem(str(query.value(2)))) 
            self.Ui_gestCaisse.vue_dec_caisse.setItem(row, 3, QTableWidgetItem(str(query.value(3)))) 
            self.Ui_gestCaisse.vue_dec_caisse.setItem(row, 4, QTableWidgetItem(str(query.value(4))))  
            



        montant = "SELECT SUM(Montant) from Decaissement where Date = "+"'"+ str(self.Ui_gestCaisse.calendrier.selectedDate().toString("yyyy-MM-dd"))+"'"
        
        query.exec_(montant)

        while query.next():

            self.Ui_gestCaisse.label_total.setText("Total : "+str(query.value(0))+" FCFA")

    def imprimer_caisse(self):
       pass
        
    def totalMontant(self):
        pass

    def TotalSomme(self):
        
        self.Ui_gestCaisse.label_total.setText("Le montant total est de : FCFA")

    ################""
    '''Gestion de la pharmacie'''

    def gestPharma(self):
        pass

    def Affiche_produit(self):
        pass
    
    def inventaire_produit(self):
        pass
  
    def list_produit(self):
        pass
  
    def Ajouter_produit(self):
        pass

    ##############
    ''' Gestion de paramettre et preferences de ... '''

    def Actualiser(self):
        self.gestPharma()
        self.gestCaisse()
        self.gestRDV()
        self.gestP()

    def gest_Parametre(self):
       
       self.Ui_para = QUiLoader().load(QFile("./vues/paramettre.ui"))

       '''fenetre utilisateur'''
       self.Ui_add_usr = QUiLoader().load(QFile("./vues/addUser.ui"))
       self.Ui_supp_usr = QUiLoader().load(QFile("./vues/delUser.ui"))
       self.Ui_mod_usr = QUiLoader().load(QFile("./vues/mod_user.ui"))
       
       '''fenetre docteur'''
       self.Ui_add_dr = QUiLoader().load(QFile("./vues/dr/addDr.ui"))
       self.Ui_supp_dr = QUiLoader().load(QFile("./vues/dr/delDr.ui"))
       self.Ui_mod_dr = QUiLoader().load(QFile("./vues/dr/mod_Dr.ui"))
       
      
       self.Ui_Acceuil.setCentralWidget(self.Ui_para)


       '''Ajout des icons ''' 
       icon = QIcon()

       icon.addFile(u"./res/user.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_add_usr.ic1.setIcon(icon)
       self.Ui_mod_usr.ic1.setIcon(icon)
        

       '''icon paramettre'''
       icon.addFile(u"./res/users.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.add_us.setIcon(icon)
       
       icon.addFile(u"./res/user.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.mod_us.setIcon(icon)
       
       icon.addFile(u"./res/user_delete.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.supp_us.setIcon(icon)

       icon.addFile(u"./res/users.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.add_dr.setIcon(icon)
       
       icon.addFile(u"./res/user.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.mod_dr.setIcon(icon)
       
       icon.addFile(u"./res/supp.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.supp_dr.setIcon(icon)
       
       icon.addFile(u"./res/lock.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_para.bloquer.setIcon(icon)

       ''' Icon  '''
       iconOk = QIcon()
       icon.addFile(u"./res/unlock.png", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_add_usr.ic2_2.setIcon(icon)
       self.Ui_mod_usr.ic2.setIcon(icon)

       icon.addFile(u"./res/ok.svg", QSize(), QIcon.Normal, QIcon.Off)
       self.Ui_add_usr.add_usr.setIcon(iconOk)
       self.Ui_supp_usr.del_usr.setIcon(iconOk)

       icon.addFile(u"./res/supp.png", QSize(), QIcon.Normal, QIcon.Off)
      
       '''lister les docteur '''
       query = QSqlQuery()
       query.exec_("select distinct * from  docteur")
       self.id_doc = {}
       self.Ui_mod_dr.list_dr.clear()
        
       while query.next():

            self.Ui_mod_dr.list_dr.addItem(str(query.value(1))+" "+str(query.value(2)))
            self.id_doc [str(query.value(1))+" "+str(query.value(2))] = str(query.value(0))
       '''Fin du listage '''

       ''' evenement paramettre'''
       self.Ui_para.mod_us.clicked.connect(self.Ui_mod_usr.show)
       self.Ui_para.add_us.clicked.connect(self.Ui_add_usr.show)
       self.Ui_para.supp_us.clicked.connect(self.Ui_supp_usr.show)
       
       ''' dr '''
       self.Ui_para.mod_dr.clicked.connect(self.Ui_mod_dr.show)
       self.Ui_para.add_dr.clicked.connect(self.Ui_add_dr.show)
       self.Ui_para.supp_dr.clicked.connect(self.Ui_supp_dr.show)
       self.Ui_add_dr.add_dr.clicked.connect(self.Ajouter_dr)
       self.Ui_supp_dr.del_dr.clicked.connect(self.supp_dr)
       self.Ui_mod_dr.mod_dr.clicked.connect(self.mod_dr)
       
       '''evenement user'''
       self.Ui_add_usr.add_usr.clicked.connect(self.Ajouter_user)
       self.Ui_supp_usr.del_usr.clicked.connect(self.supp_user)
        
       self.Afficher_user()
   
    def prix_consultation(self):
        pass


    #############
    ''' Gestion Authentification et utilisateurs '''

    def login(self):
        if (self.session(self.Ui_con.nom_u.text(), self.Ui_con.mdp_u.text())):
            
            self.Ui_con.close()

            self.Ui_Acceuil.show()
        else:

          
            self.__init__()

    def session(self, nom, mdp):

        query = QSqlQuery()
        query.exec_("Select * from User where u_nom = '"+str(nom)+"' And u_mdp = '"+str(mdp)+"'")
        cpt = 0
        while query.next():
            cpt = cpt +1

        if(self.Ui_con.nom_u.text() == "" and self.Ui_con.mdp_u.text() == "" ):
            self.msg.setWindowTitle("Oups....")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText(" Veuillez remplir les champs  ")
            self.msg.exec_()
          
            return False
        elif(cpt<1):

            self.msg.setWindowTitle("Oups....")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText(" Nom d'utilisateur ou mot de passe incorrecte  ")
            self.msg.exec_()
           
            return False
        else:
            self.msg.setText(" Connexion reussi")
            self.msg.exec_()
            
            self.Ui_con.close()
           
            return True

    def Ajouter_user(self):
        
        query = QSqlQuery()
        query.prepare("INSERT INTO user (u_nom, u_mdp, idDroit) VALUES ( ?, ?, ?)")

        query.bindValue(0, str(self.Ui_add_usr.u_name.text()))
        query.bindValue(1, str(self.Ui_add_usr.u_mdp.text()))
        
        if( self.Ui_add_usr.pc.isChecked()):
             query.bindValue(2, int(2))
        elif( self.Ui_add_usr.rdv.isChecked()):
             query.bindValue(2, int(3))
        elif( self.Ui_add_usr.usr.isChecked()):
             query.bindValue(2, int(4))
        elif( self.Ui_add_usr.phar.isChecked()):
             query.bindValue(2, int(5))
        else:
            query.bindValue(2, int(1))
        
        v = query.exec_()
        
        if(v):
            self.msg.setText("Nouvel Utilisateur enregistrer")
            self.msg.exec_()
            self.Ui_add_usr.close()
            self.Afficher_user()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.setText("Echec Enregistrement utilisateur "+str(query.lastError()))
            self.msg.exec_()

    def user_en_cours(self):
        pass

    def Afficher_user(self):
        
        query = QSqlQuery()
        query.exec_("SELECT * from user where u_nom != 'root' ")

        self.id_ = {}
        

        self.Ui_supp_usr.list_usr.clear()
        self.Ui_mod_usr.list_usr.clear()
        while query.next(): 

            self.Ui_supp_usr.list_usr.addItem(str(query.value(1)))
            self.Ui_mod_usr.list_usr.addItem(str(query.value(1)))  
            self.id_ [str(query.value(1))] = str(query.value(0))

        print(self.id_)


    '''Users'''

    def supp_user(self):

        self.Afficher_user()
        query = QSqlQuery()
        query.prepare("DELETE from user where idUser = ? ")

        query.bindValue(0, str(self.id_ [self.Ui_supp_usr.list_usr.currentText()]))
      
        v = query.exec_()
        
        if(v):
            self.msg.setText("Utilisateur Supprimer")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            self.Ui_supp_usr.close()
            self.Afficher_user()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Echec suppression utilisateur "+str(query.lastError()))
            self.msg.exec_()

    def mod_user(self):
        
        self.Afficher_user()
        
        query = QSqlQuery()
        query.prepare("SELECT * from user where idUser = ? ")

        query.bindValue(0, str(self.id_ [self.Ui_mod_usr.list_usr.currentText()]))

        query.exec_()

        while query.next():
            self.Ui_mod_usr.u_name.setText(str(query.value(1)))
            self.Ui_mod_usr.u_mdp.setText(str(query.value(2)))

      
        v = query.exec_()
        
        if(v):
            self.msg.setText("Utilisateur modifier")
            self.msg.exec_()
            self.Ui_supp_usr.close()
            self.Afficher_user()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Echec modification utilisateur "+str(query.lastError()))
            self.msg.exec_()
   
    '''
    def supp_user(self):
        
        self.Afficher_user()
        query = QSqlQuery()
        query.prepare("DELETE from user where idUser = ? ")

        query.bindValue(0, str(self.id_ [self.Ui_supp_usr.list_usr.currentText()]))
      
        v = query.exec_()
        
        if(v):
            self.msg.setText("Utilisateur Supprimer")
            self.msg.exec_()
            self.Ui_supp_usr.close()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Echec suppression utilisateur "+str(query.lastError()))
            self.msg.exec_()
    '''

    '''Docteur '''
    
    def Ajouter_dr(self):
        
        query = QSqlQuery()
        query.prepare("INSERT INTO docteur (nomDoc, prenomDoc) VALUES (?, ?)")

        query.bindValue(0, str(self.Ui_add_dr.dr_nom.text()))
        query.bindValue(1, str(self.Ui_add_dr.dr_prenom.text()))
        
        
        v = query.exec_()
        
        if(v):
            self.msg.setText("Docteur Ajouter")
            #self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.exec_()
            self.Ui_add_usr.close()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Docteur non ajouter "+str(query.lastError()))
            self.msg.exec_()

    def supp_dr(self):
    
        v = query.exec_()
        
        if(v):
            self.msg.setText("Utilisateur Supprimer")
            self.msg.exec_()
            self.Ui_supp_usr.close()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Echec suppression utilisateur "+str(query.lastError()))
            self.msg.exec_()

    def mod_dr(self):

        '''Mod fu Docteur'''
        
        query = QSqlQuery()
        query.prepare("Update docteur set nomDoc = ?, prenomDoc = ? where idDoc = ? ")
            
        query.bindValue(0, str(self.Ui_mod_dr.dr_nom.text()))
        query.bindValue(1, str(self.Ui_mod_dr.dr_prenom.text()));
        query.bindValue(2, int(self.id_doc [self.Ui_mod_dr.list_dr.currentText()]))
 
        v = query.exec_()
        
        if(v):
            self.msg.setText("Docteur supprimer")
            #self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.exec_()
            self.Ui_mod_dr.close()
           
        else:
            self.msg.setWindowTitle("Erreur!!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setText("Echec de suppression du doceur "+str(query.lastError()))
            self.msg.exec_()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    davina = Application()

    sys.exit(app.exec_())
