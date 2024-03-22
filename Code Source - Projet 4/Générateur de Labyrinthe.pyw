from __future__ import annotations
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
from matplotlib.patches import Rectangle

import time
import numpy as np
from typing import List,Union
from Labyrinthe import *
from AffichageGraphique import *

class Windows(ctk.CTk):
    def __init__(self,theme: str,tcolor: str,taille: str):
        """ fenètre de base de l'application """
        super().__init__()
        self.geometry(taille) #on definie la taille de la fenètre
        self.taille = taille 
        self.title('Générateur de Labyrinthe') #on definie le titre de la fenètre
        self.protocol("WM_DELETE_WINDOW", self.quitw) #le protocol de fermeture de la fnètre
        self.wm_title("Générateur de Labyrinthe") #on definie le titre de la fenètre tkinter
        try:
            self.iconbitmap('images\\icone.ico') #on définie l'icone de la fenètre
        except:
            pass # si une erreur survient lors de l'import de l'icone on ne change pas l'icone, ce sera celle de base
        self.framemain = MainTK(self) # on gènre les diférentes frames de notre application
        self.framegen = GenererTK(self)
        self.framelaby = LabyTK(self)
        self.framegraph = GraphTK(self)
        self.framepara = Parametre(self)
        self.framemain.pack(fill='both', expand=True) #on affiche la fenètre principal framemain
        try : #lecture du fichier des préférences
            errors = 0
            f=open('preférences.config')
            lines=f.readlines()
            if len(lines[0].split(',')) >= 7 : #on lit le fichier preférences.config et on donne les valeurs contenue dans le fichier a un dictionnaire contenue dans la class Parametre
                colorsdict = {'3': None, '4': None, '5': None}
                for i in range(3,6):
                    if is_color_like(lines[0].split(',')[i]) and lines[0].split(',')[i] != 'None': # on verifie que les element sont des couleurs
                        colorsdict[str(i)] = lines[0].split(',')[i]
                    elif not is_color_like(lines[0].split(',')[i]):
                        errors += 1
                conversion = {'3':'nodes', '4':'edges', '5':'background'}
                for ncolors in conversion: #on convertie les element recu avec les valeur dans le dictionnaire
                    self.framepara.graphcolors[conversion[ncolors]] = colorsdict.get(ncolors, None)
                check = lines[0].split(',')[6]
                if check == 'True' : #on donne la valeur de la pondération 
                    self.framepara.graphcolors['pond'] = True
                else :
                    self.framepara.graphcolors['pond'] = False
            if len(lines[0].split(',')) < 7 or errors != 0: 
                if errors != 0 : #si il y'a des erreurs alors on affiche une erreur
                    messagebox.showerror('Erreur Préférences', f'{errors} valeurs du fichier config non lisibles, Veleurs remise par défault')
                else : #si le fichier n'est pas lisible on envoie une erreur
                    messagebox.showerror('Erreur Préférences', 'Les valeurs du fichier config ne sont pas lisibles, elle on été remise par défault') 
                with open('preférences.config','w') as file: #on lance le programe avec des valeurs par défaut
                        file.write(f"{theme},{tcolor},{taille}")
                        for elem in self.framepara.graphcolors.keys() :
                            file.write(',')
                            file.write(str(self.framepara.graphcolors.get(elem, None)))
        except: #si le code echoue on lance le programe avec des valeurs par défaut et on affiche une erreur
            messagebox.showerror('Erreur Préférences', 'Les valeurs du fichier config ne sont pas lisibles, elle on été remise par défault') 
            self.framepara.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False}
            with open('preférences.config','w') as file:
                        file.write(f"{theme},{tcolor},{taille},None,None,None,False")
        

    def changeframe(self,frame: Union[LabyTK,MainTK,GraphTK,GenererTK,Parametre]):
        """fonction qui change la frame affichée"""
        self.framemain.pack_forget()
        self.framegraph.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        frame.pack(side="top", fill="both", expand=True)

    def changewithclear(self, frame: Union[LabyTK,MainTK,GraphTK,GenererTK,Parametre]):
        """fonction qui change la frame affichée en supprimant les élément de la frame du graph et du labyrinthe"""
        self.framemain.pack_forget()
        self.framegraph.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        for widgets in self.framegraph.winfo_children():
            widgets.destroy()
        for widgets in self.framelaby.winfo_children():
            widgets.destroy()
        frame.pack(side="top", fill="both", expand=True)

    def changewithclearall(self, frame: Union[LabyTK,MainTK,GraphTK,GenererTK,Parametre]):
        """fonction qui change la frame affichée en supprimant tout les element de toute les frames"""
        self.framemain.pack_forget()
        self.framegraph.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        for widgets in self.framemain.winfo_children():
            widgets.destroy()
        for widgets in self.framegen.winfo_children():
            widgets.destroy()
        for widgets in self.framepara.winfo_children():
            widgets.destroy()
        for widgets in self.framegraph.winfo_children():
            widgets.destroy()
        for widgets in self.framelaby.winfo_children():
            widgets.destroy()
        self.framemain.initialisation()
        self.framegen.initialisation()
        self.framepara.initialisation()
        frame.pack(side="top", fill="both", expand=True)
    
    def quitw(self):
        """méthode qui quitte le code"""
        plt.close('all') 
        plt.ioff()
        self.quit()
        self.destroy()
        quit()

class MainTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page principal"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()

    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        titre(self,'Générateur de Labyrinthe')
        button(self,'Générer un labyrinthe',lambda : self.parent.changeframe(self.parent.framegen))
        button(self,'Importer un labyrinthe',self.importer)
        button(self,'Paramètres',lambda : self.parent.changeframe(self.parent.framepara))
        button(self,'Quitter',self.parent.quit)

    def importer(self):
        """fonction qui permet l'import d'un labyrinthe"""
        try:
            filetypes = (('text files', '*.txt'),) #définition des type de fichier acceptée
            nom = fd.askopenfilename(title='Ouvrire un fichier Texte',filetypes=filetypes,defaultextension="*.txt") #nom prend la valeur du chemin d'accès du fichier
            if nom == '' or None : #si le chemin est vide arreter la fonction
                return
            with open(nom,'r') as file: #on lit le fichier séléctionnée
                ligne = file.read()
            names = [elm for elm in ligne.split('|')[0].split(';')] #on lit la liste des noms
            poid = list(zip(ligne.split('|')[1].split(';'),ligne.split('|')[2].split(';'),ligne.split('|')[3].split(';'))) #on lit 3 liste une pour chaque noeud de l'arrete et une pour le poid que l'on zip en une liste de tuple
            names.pop() #on supprime le dernier elment de la liste
            poid.pop() #on supprime le dernier elment de la liste
            labyimport = Labyrinthe(int(ligne.split('|')[4]),int(ligne.split('|')[5]),False)  #on creer un labyrinthe de taille egal a celle du labyrinthe du fichier
            if int(ligne.split('|')[5]) < 2 and int(ligne.split('|')[4]) < 2 : #on verifie les donnée du labyrinthe
                return 
            graph = Graph_Weighted() #on créer un graphe vide
            graph.from_dict_list(names,poid) #on importe les noeud et les arretes dans ce graphe
            labyimport.grillevide = graph #on defini le graph du labyrinthe crée tout a l'heure
            labyimport.debut = ligne.split('|')[6] #on lit le début
            labyimport.fin = ligne.split('|')[7] #on lit le la fin
            labyimport.casecoin = ligne.split('|')[8] #ainsi que le coin et on les initialise comme valeur pour le labyrinthe
            self.parent.framelaby.laby = labyimport #on défini le labyrinthe utilisé par la frame du labyrinthe 
            self.parent.framelaby.generer(int(ligne.split('|')[4]),int(ligne.split('|')[5]),False) #on générer le labyrinthe sans le générer aléatoirement
        except: #si le code echoue on reviens au menu principal et on montre 
            self.parent.changewithclearall(self)
            messagebox.showerror('Erreur', "Une erreur est survenue lros de l'importation") 

class Parametre(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page des paramètre"""
        super().__init__(parent)
        self.parent = parent
        self.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False} #on initilalise le dictionaire des valeurs
        self.graphcolorssave = {'nodes': None, 'edges': None, 'background': None, 'pond': False} #on initilalise le dictionaire des valeurs courantes
        self.initialisation()

    def initialisation(self):
        try : #on ouvre le fichier config pour recuperer les valeur de configuration de l'application
            f=open('preférences.config')
            lines=f.readlines()
            c1 = {"light":'Clair',"dark":'Sombre',"system":'Système'}
            c2 = {"blue":'Bleu',"dark-blue":'Bleu Sombre',"green":'Vert'}
            c3 = {'1920x1080':'1920x1080','1080x720':'1080x720','1020x760':'1020x760','855x620':'855x620'}
            selectthemedef = c1.get(lines[0].split(',')[0], 'Sombre')
            selectcolordef = c2.get(lines[0].split(',')[1], 'Bleu')
            selecttailledef = c3.get(lines[0].split(',')[2], '1080x720')
            check = lines[0].split(',')[6]
            if check == 'True' :
                check = True
            else :
                check = False
        except:
            selectthemedef = 'Sombre'
            selectcolordef = 'Bleu'
            selecttailledef = '1080x720'
            check = False
        #affichage et assignations des éléments de la fenètre
        titre(self,'Paramètres')
        selecttheme = selection(self,"Thème de l'application :", ['Clair','Sombre','Système'], selectthemedef)
        selectcolor = selection(self,'Couleur du Thème :', ['Bleu','Bleu Sombre','Vert'], selectcolordef)
        selecttaille = selection(self,'Taille de la fenètre :', ['1920x1080','1080x720','1020x760','855x620'], selecttailledef)
        text(self,'Apparence du Graph : ')
        choosecolors(self,'Couleur des Noeuds : ', lambda: self.colorpick('nodes'))
        choosecolors(self,'Couleur des Arretes : ', lambda: self.colorpick('edges'))
        choosecolors(self,'Couleur de Fond : ', lambda: self.colorpick('background'))
        text(self,'Apparence du Labyrinthe : ')
        x = checkbox(self,'Afficher la pondération', lambda: self.check('pond', x.get()), True, False,check)
        multiple_button(self,2,['Menu Principal', 'Appliquer'],[self.menuprincipal, lambda: self.validation(selecttheme.get(),selectcolor.get(),selecttaille.get())])
        button(self,'Revenir aux paramètres par défaut', self.reset)
        text(self,"Générateur de Labyrinthe, deltahmed, version 1.0", 10)
    
    def reset(self) :
        """méthode qui remet les paramètres par défault"""
        message = messagebox.askokcancel('Reset des paramètres !',"Vous êtes sur le point de réinitialiser vos paramètres voulez vous continuer ?")
        if message :
            self.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False}
            self.validation('Sombre','Bleu','1080x720')

    def menuprincipal(self) :
        """méthode pour revenir au menu principal"""
        message = messagebox.askokcancel('retour au menu',"Toute modification non appliquée ne sera pas prise en compte, voulez vous continuer ?")
        if message :
            self.parent.changeframe(self.parent.framemain)

    def colorpick(self,index: int):
        """méthode appelé lors du chois de couleur"""
        colors = askcolor(title="Choisir une couleur")
        self.graphcolorssave[index] = colors[1]

    def check(self, index: int, val: Union[str,int,float,None,bool]):
        """méthode appelé lors de la coche d'une case"""
        self.graphcolorssave[index] = val

    def validation(self,apmode: str,colormode: str, taillemode: str):
        """méthode qui valide et enregistre les paramètres"""
        self.graphcolors = self.graphcolorssave #on actualise le dictionnaire des paramètres
        c1 = {'Clair':"light",'Sombre':"dark",'Système':"system"}
        c2 = {'Bleu':"blue",'Bleu Sombre':"dark-blue",'Vert':"green"}
        c3 = {'1920x1080':'1920x1080','1080x720':'1080x720','1020x760':'1020x760','855x620':'855x620'}
        ctk.set_appearance_mode(c1.get(apmode, "dark")) #on change le thème
        ctk.set_default_color_theme(c2.get(colormode, "blue")) #on change le thème
        self.parent.geometry(taillemode) #on change la taille
        self.parent.taille = taillemode
        with open('preférences.config','w') as file:   #on ecrit le tout dans le fichier config
            file.write(c1.get(apmode, "dark"))
            file.write(',')
            file.write(c2.get(colormode, "blue"))
            file.write(',')
            file.write(c3.get(taillemode, "1080x720"))
            for elem in self.graphcolors.keys() :
                file.write(',')
                file.write(str(self.graphcolors.get(elem, None)))
        self.parent.changewithclearall(self.parent.framepara) #on actualise la fenetre
    
class GenererTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """fenètre de génération"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()
    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        titre(self, 'Générer un labyrinthe')
        text(self, 'Hauteur :')
        self.e_hauteur = champ(self)
        self.e_hauteur.pack()
        text(self, 'Longueur :')
        self.e_longueur = champ(self)
        self.e_longueur.pack()
        button(self, 'Générer', lambda: self.parent.framelaby.generer(self.e_hauteur.get(),self.e_longueur.get(),True))
        multiple_button(self,2, ['Menu Principal','Reset'], [lambda: self.parent.changeframe(self.parent.framemain), self.reset])

    def reset(self):
        """fonction qui reset la page"""
        for widgets in self.winfo_children():
            widgets.destroy()
        self.initialisation()
            
    
class GraphTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """fenètre de génération"""
        super().__init__(parent)
        self.parent = parent
    
    def getgraph(self):
        """méthode qui permet l'optention d'un graph a partir du labyrinthe généré"""
        self.buttuns = multiple_button(self,4,['Menu principal','Afficher le Labyrinthe','Solutions et parcours','Enregister'],[self.parent.framelaby.menuprincipal ,self.parent.framelaby.getlaby,self.parent.framelaby.menuderoulant,self.parent.framelaby.enregistrer])
        fig = Figure()
        ax = fig.add_subplot()
        graphnx = nx.Graph(self.parent.framelaby.dic) #on creer le graph networkx
        if ctk.get_appearance_mode() == "Light": #on choisit les couleur en fonction des préférences
            fig.set_facecolor('#DBDBDB')
            if self.parent.framepara.graphcolors.get('background', None) != None:
                ax.set_facecolor(self.parent.framepara.graphcolors.get('background', '#DBDBDB'))
            else : ax.set_facecolor('#DBDBDB')
            edgecolor = self.parent.framepara.graphcolors.get('edges', None)
            nodescolor = self.parent.framepara.graphcolors.get('nodes', None)
        if ctk.get_appearance_mode() == "Dark" :
            fig.set_facecolor('#2B2B2B')
            if self.parent.framepara.graphcolors.get('background', None) != None:
                ax.set_facecolor(self.parent.framepara.graphcolors.get('background', '#2B2B2B'))
            else : ax.set_facecolor('#2B2B2B')
            if self.parent.framepara.graphcolors.get('edges', None) == None:
                edgecolor = 'white'
            else :
                edgecolor = self.parent.framepara.graphcolors.get('edges', None)
            if self.parent.framepara.graphcolors.get('nodes', None) == None :
                nodescolor = '#4CA4E0'
            else : nodescolor = self.parent.framepara.graphcolors.get('nodes', None)
        nx.draw_networkx(graphnx, #on dessine le graph dans la fenètre
                        pos=self.parent.framelaby.laby.getpos(),
                        ax=ax,
                        with_labels=False,
                        node_shape=None, 
                        node_color=nodescolor,
                        edge_color=edgecolor)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw() #on affiche le tout dans tkinter
        toolbar = toolbarmatplotlib(canvas,self) #on creer la barre de navigation matplotlib
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        toolbar.pack(fill=tk.X)
        self.parent.changeframe(self.parent.framegraph)

class LabyTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """page d'affichage du labyrinthe"""
        super().__init__(parent)
        self.parent = parent
        self.menu = False
        self.retourmenu = False
        self.ponder = False
        self.annim = False

    def menuprincipal(self):
        """méthodes qui retourne aux menu principal"""
        message = messagebox.askokcancel('retour au menu',"Toute modification non appliquée ne sera pas prise en compte, voulez vous continuer ?")
        if message : #si on accepte 
            self.retourmenu = True
            plt.close('all') #on ferme les fenetre matplolib
            plt.ioff()
            self.framemenud.place(relx=-1, rely=-1, anchor='ne') #on cache le menu deroulant
            self.parent.changewithclear(self.parent.framemain) #on change de frame
    
    def menuderoulant(self):
        """affichage du menu déroulant"""
        if self.menu :
            self.menu = False
            self.framemenud.place(relx=-1, rely=-1, anchor='ne')
        else :
            self.menu = True
            self.framemenud.place(relx=1, rely=0.1, anchor='ne')
            
    
    def enregistrer(self):
        """enregistrer un labyrinthe"""
        try : 
            filetypes = (('text files', '*.txt'),) #définition des type de fichier acceptée
            nom = fd.asksaveasfilename(title='Enregistrer un fichier Texte',filetypes=filetypes,defaultextension="*.txt") #nom prend la valeur du chemin d'accès du fichier
            names = ''.join(map(lambda x: str(x)+';',list(self.laby.getgraph().__dict__()))) #on enregistre chaque élément separement 
            l1 = ''.join(map(lambda x: str(x)+';',[el[0] for el in self.laby.getgraph().poids]))
            l2 = ''.join(map(lambda x: str(x)+';',[el[1] for el in self.laby.getgraph().poids]))
            l3 = ''.join(map(lambda x: str(x)+';',[el[2] for el in self.laby.getgraph().poids]))
            l4 = ''.join(map(lambda x: '|'+ str(x),[self.laby.hauteur, self.laby.longueur, self.laby.getdebut(), self.laby.getfin(), self.laby.getcoin()]))
            with open(nom,'w') as file: #on ecrit le tout grace a des séparateur
                file.write(names)
                file.write('|')
                file.write(l1)
                file.write('|')
                file.write(l2)
                file.write('|')
                file.write(l3)
                file.write(l4)
        except : #si le code echoue alors envoyer une erreur
            messagebox.showerror('Erreur', "Une erreur est survenue lorsde l'enregistrement du fichier") 

    def generer(self, hauteur: Union[str,int], longueur: Union[str,int], gen: bool):
        '''générer le labyrinthe et l'afficher'''
        if gen : # si on génére le labyrinthe alors
            try: # on verifie que les valeur sont correcte 
                h = int(hauteur)
                l = int(longueur)
                if h <= 1 or l <= 1 : #si le labyrinthe est trop petit, renvoyer une erreur
                    messagebox.showerror('Valeur incorectes', 'entiers naturels positifs supérieur a 1 requis') 
                    return
            except ValueError:# si la valeur n'est pas au bon format renvoyer une erreur
                messagebox.showerror('Valeur incorectes', 'Valeur numérique requise (entiers naturels positifs supérieur a 1)') 
                return

        else :
            #si on importe la labyrinthe on met a jour les valeurs
            h = int(hauteur)
            l = int(longueur)
            if h <= 1 or l <= 1 :
                messagebox.showerror('Erreur', 'Erreur de donnée') 
                return 
        message = 'yes'
        if h > 30 and l > 30 : #si le labyrinthe fait plus de 30x30 cases avertir l'utilisateur
            message = messagebox.askokcancel('Génération longue', 
            f"La génération d'un labyrinthe de taille {h}x{l} peut prendre du temps en fonction de la puissance de votre ordinateur, Les images devenant trop petites,le depart sera donc noté par un point vert, et l'arrivée par un point rouge, voulez vous continuer ?")
        if h > 50 and l > 50 :#si le labyrinthe fait plus de 50x50 cases avertir l'utilisateur
            message = messagebox.askokcancel('Performances', 
            f"Generer un labyrinthe de plus de 50x50 peut entrainer de gros soucis de performance, voulez vous continuer ?")
        if message :
            if gen : # si on génére un labyrinthe alors le générer
                self.laby = Labyrinthe(h,l)
                self.laby.grillevide.re_ponderation_aleatoire(randint(10,100)) # on donne une pondération aléatoire
            self.dic = self.laby.__dict__()
            self.menu = False #variable de l'affichage du menu
            #on configure tout les élément a afficher a l'ecrant
            self.buttuns = multiple_button(self,4,['Menu principal','Afficher le Graph','Solutions et parcours','Enregister'],[self.menuprincipal ,self.parent.framegraph.getgraph,self.menuderoulant,self.enregistrer])
            fig1 = Figure()
            ax1 = fig1.add_subplot()
            ax1.set_aspect('equal', adjustable='box')
            ax1.set_axis_off()
            if ctk.get_appearance_mode() == "Light": # on change la couleur en fonction du thème 
                fig1.set_facecolor('#DBDBDB')
                plotcases(ax1, self.laby, 'k',h,l,self.parent.framepara.graphcolors.get('pond',False)) #on affiche les cases
            if ctk.get_appearance_mode() == "Dark" :
                fig1.set_facecolor('#2B2B2B')
                plotcases(ax1, self.laby, 'w',h,l,self.parent.framepara.graphcolors.get('pond',False)) #on affiche les cases
            fig1.subplots_adjust(0,0,1,1)
            coin = self.laby.getcoin() #on ajuste l'affichage en fonction de la taille du labyrinthe, l'affichage sera concentré sur la case du début
            if coin == f'{0},{0}': xmin,ymin,xmax,ymax = -1,-1,50,50
            if coin == f'{l-1},{h-1}': xmin,ymin,xmax,ymax = l-50,h-50,l,h
            if coin == f'{0},{h-1}': xmin,ymin,xmax,ymax = -1,h-50,50,h
            if coin == f'{l-1},{0}': xmin,ymin,xmax,ymax = l-50,-1,l,50
            if h > 70 or l > 70 : #si le labyrinthe fait plus de 70x70 ajuster l'affichage pour que les case ne soit pas trop petites
                text(self, "le labyrinthe n'est pas affiché entièrement, utiliser l'outils de déplacement pour explorer le labyrinthe, pour bloquer le déplacement, maintenir x ou y",12)
                if h > 70 and l > 70 :
                    ax1.axis([xmin, xmax, ymin, ymax])
                if h > 70 and l < 70 :
                    ax1.axis([-1, l, ymin, ymax])
                if h < 70 and l > 70 :
                    ax1.axis([xmin, xmax, -1, h])
            canvas1 = FigureCanvasTkAgg(figure=fig1, master=self)
            canvas1.draw() # on affiche le canvas dans tkinter
            toolbar1 = toolbarmatplotlib(canvas1,self) #on creer la barre d'outils matplot lib
            canvas1.get_tk_widget().pack(expand=True, fill=tk.BOTH)
            self.framemenud = menubox(self.parent,'Menu Solution/Parcours','Scrollez pour decouvrire toutes les options', #on creer notre menu déroulant avec la fonction creer pour l'ocasion
                                        ('Parcours :',None),
                                        ('Parcours en largeur',lambda: self.laby_parcours_largeur(canvas1,ax1,fig1,h,l)),
                                        ('Parcours en largeur recursif',lambda: self.laby_parcours_largeur_rec(canvas1,ax1,fig1,h,l)),
                                        ('Parcours en profondeur aleatoire',lambda: self.laby_parcours_profondeur_alea(canvas1,ax1,fig1,h,l)),
                                        ('Parcours en profondeur',lambda: self.laby_parcours_profondeur_fixe(canvas1,ax1,fig1,h,l)),
                                        ('Parcours en profondeur recursif',lambda: self.laby_parcours_profondeur_rec(canvas1,ax1,fig1,h,l)),
                                        ('Cycles :',None),
                                        ('Detection de cycles',lambda: self.laby_cycle(canvas1,ax1,fig1,h,l)),
                                        ('Détéction de cycles matrice',lambda: self.laby_cycle_matrice(canvas1,ax1,fig1,h,l)),
                                        ('Solutions :',None),
                                        ('Solution parcours largeur',lambda: self.solution_parcours_largeur(canvas1,ax1,fig1,h,l)),
                                        ('Solution parcours largeur recursif',lambda: self.solution_parcours_largeur_rec(canvas1,ax1,fig1,h,l)),
                                        ('Solution parcours profondeur',lambda: self.solution_parcours_profondeur(canvas1,ax1,fig1,h,l)),
                                        ('Solution parcours profondeur recursif',lambda: self.solution_parcours_profondeur_rec(canvas1,ax1,fig1,h,l)),
                                        ('Algorithme de dijkstra :',None),
                                        ('Algorithme de dijkstra aléatoire',lambda: self.laby_dijkstra_alea(canvas1,ax1,fig1,h,l)),
                                        ('Algorithme de dijkstra (poid de 1)',lambda: self.laby_dijkstra_poid(canvas1,ax1,fig1,h,l)),
                                        ('Graph :',None),
                                        ('Repondération aléatoire',lambda: self.graphrepond(ax1,fig1,h,l,canvas1)),
                                        ('Afficher Graph Pondéree', self.graphpond),
                                        ('Labyrinthe :',None),
                                        ('Activer pondération',lambda: self.labypond(ax1,fig1,h,l,canvas1))
                                        )
            toolbar1.pack(fill=tk.X)
            self.parent.changeframe(self.parent.framelaby) #on actualise l'affichage, on affiche la frame du labyrinthe

    def getlaby(self): 
        """fonction qui actualise le boutton de l'affichage du graph et affiche le labyrinthe"""
        self.buttuns[1].configure(command=lambda: self.parent.changeframe(self.parent.framegraph))
        self.parent.changeframe(self.parent.framelaby)
    
    def clear(self,ax1,fig1,h: int,l: int,canvas):
        """fonction qui supprime tout les éléent ajouté"""
        ax1.cla()
        ax1.set_aspect('equal', adjustable='box')
        ax1.set_axis_off()
        if ctk.get_appearance_mode() == "Light": # on change la couleur en fonction du thème 
            fig1.set_facecolor('#DBDBDB')
            plotcases(ax1, self.laby, 'k',h,l,self.parent.framepara.graphcolors.get('pond',False)) #on affiche les cases
        if ctk.get_appearance_mode() == "Dark" :
            fig1.set_facecolor('#2B2B2B')
            plotcases(ax1, self.laby, 'w',h,l,self.parent.framepara.graphcolors.get('pond',False)) #on affiche les cases
        fig1.subplots_adjust(0,0,1,1)
        coin = self.laby.getcoin() #on ajuste l'affichage en fonction de la taille du labyrinthe, l'affichage sera concentré sur la case du début
        if coin == f'{0},{0}': xmin,ymin,xmax,ymax = -1,-1,50,50
        if coin == f'{l-1},{h-1}': xmin,ymin,xmax,ymax = l-50,h-50,l,h
        if coin == f'{0},{h-1}': xmin,ymin,xmax,ymax = -1,h-50,50,h
        if coin == f'{l-1},{0}': xmin,ymin,xmax,ymax = l-50,-1,l,50
        if h > 70 or l > 70 : #si le labyrinthe fait plus de 70x70 ajuster l'affichage pour que les case ne soit pas trop petites
            text(self, "le labyrinthe n'est pas affiché entièrement, utiliser l'outils de déplacement pour explorer le labyrinthe, pour bloquer le déplacement, maintenir x ou y",12)
            if h > 70 and l > 70 :
                ax1.axis([xmin, xmax, ymin, ymax])
            if h > 70 and l < 70 :
                ax1.axis([-1, l, ymin, ymax])
            if h < 70 and l > 70 :
                ax1.axis([xmin, xmax, -1, h])
        canvas.draw() # on actualise le canvas dans tkinter

    def graphrepond(self,ax,fig1,h: int,l: int,canvas):
        """repondération aléatoire du labyrinthe"""
        self.laby.grillevide.re_ponderation_aleatoire(randint(10,100))
        self.clear(ax,fig1,h,l,canvas)

    def labypond(self,ax,fig1,h,l,canvas):
        """affichage de la pondéartaion"""
        self.parent.framepara.graphcolors['pond'] = True
        self.clear(ax,fig1,h,l,canvas)

    def graphpond(self):
        """ouverture et affichage du graph pondéré dans matplotlib""" 
        F=nx.Graph()
        F.add_nodes_from([(x) for x in list(self.laby.__dict__())])
        F.add_weighted_edges_from(self.laby.grillevide.poids)
        pos=dict()
        for elm in self.laby.grillevide.graph.keys():
            pos[elm] = (nomx(elm),nomy(elm))
        nx.draw(F,pos)
        labels = nx.get_edge_attributes(F,'weight') 
        nx.draw_networkx_edge_labels(F,pos,edge_labels=labels)
        plt.show() #on affiche cela dans une nouvelle fentre matplotlib car actualiser le canvas ne fonctionnera pas

    def annimer(self,parcours: List[str],canvas,ax,fig1,h: int,l: int,ar: bool=True):
        """annime des points a partire d'une liste de points"""
        self.retourmenu = False #on defini retour menu a false
        self.clear(ax,fig1,h,l,canvas) #remise a 0 du labyrinthe
        arrivee = False  # on defini ll'arrivé a false
        n = 0 #on defini n le nombre de points plot
        for sommet in parcours : #pour tout les sommet dans le parcours
            if self.retourmenu : #si on retourne aux menu on casse la boucle
                break
            if sommet == self.laby.getfin(): #si l'arrivé est atteinte on change la valeur d'arivée
                arrivee = True
            if sommet == self.laby.getdebut(): #si le sommet est egal au sommet de depart alors afficher un point vert
                ax.plot(nomx(sommet), nomy(sommet), marker="o", markersize=10, color="#06D6A0")
                n += 1 #on ajoute a n, 1
            elif arrivee and ar: #si on est arrivé a la fin et que l'on demande le changement de couleur grace au paramètre ar
                ax.plot(nomx(sommet), nomy(sommet), marker="o", markersize=10, color="#E5383B") #on plot un point en rouge
                n += 1 #on ajoute a n, 1
            else: #sinon on plot un point en bleu 
                ax.plot(nomx(sommet), nomy(sommet), marker="o", markersize=10, color="#3A86FF")
                n += 1 #on ajoute a n, 1
            if n%round(0.00632072*(max(h,l)**2)-0.048519*max(h,l)+1.09761) == 0 : #formule trouvée par tatonnment qui permet de calculer ne nombre de point a afficher d'un coup 
                canvas.draw() #on affiche le tout dans le canvas, cette metode est très couteuse en ressources c'est pour cela qu'on doit calculer le nombre de poit a afficher
                canvas.flush_events()
                time.sleep(0.008)
            elif len(parcours) - n < round(0.00632072*(max(h,l)**2)-0.048519*max(h,l)+1.09761) or n == 0: #on affiche le reste des points 
                canvas.draw() 
                canvas.flush_events()
                time.sleep(0.008)
        self.annim = False #on termine l'annimation


    def laby_parcours_largeur(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours en largeur"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().parcours_largeur(self.laby.getdebut())
            self.annimer(parcours,canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def laby_parcours_largeur_rec(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours en largeur recurcif"""
        try :
            if not self.annim : 
                self.annim = True
                parcours = self.laby.getgraph().parcours_largeur_rec(self.laby.getdebut())
                self.annimer(parcours,canvas,ax,fig1,h,l)
            else :
                messagebox.showinfo('Annimation','un annimation est déja en cours')
        except RecursionError : #si il y'a trop d'appel recursif ne rien afficher
            self.annim = False
            messagebox.showerror('Recursivité',"Un labyrinthe de cette taille ne peut pas se resoudre recursivement (trop d'appel recursif)")

    def laby_parcours_profondeur_alea(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours en profondeur aleatoire"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().parcours_profondeur_alea(self.laby.getdebut())
            self.annimer(parcours,canvas,ax,fig1,h,l,False)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def laby_parcours_profondeur_fixe(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours en profondeur"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().parcours_profondeur_bis(self.laby.getdebut())
            self.annimer(parcours,canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def laby_parcours_profondeur_rec(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours en profondeur recursif"""
        try:
            if not self.annim : 
                self.annim = True
                parcours = self.laby.getgraph().parcours_profondeur_rec(self.laby.getdebut())
                self.annimer(parcours,canvas,ax,fig1,h,l)
            else :
                messagebox.showinfo('Annimation','un annimation est déja en cours')
        except RecursionError : #si il y'a trop d'appel recursif ne rien afficher
            self.annim = False
            messagebox.showerror('Recursivité',"Un labyrinthe de cette taille ne peut pas se resoudre recursivement (trop d'appel recursif)")

    def laby_cycle(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours qui determine si le graph est cyclique, affiche un message si il l'est ou non"""
        if not self.annim : 
            self.annim = True
            cycle = self.laby.getgraph().EstCyclique(self.laby.getdebut())
            self.annimer(cycle[1],canvas,ax,fig1,h,l,False)
            if cycle[0]:
                messagebox.showinfo('Détéction de cycle', 'le graphe du labyrinthe est cyclique')
            else :
                messagebox.showinfo('Détéction de cycle', 'le graphe du labyrinthe est acyclique')
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def laby_cycle_matrice(self,canvas,ax,fig1,h: int,l: int):
        """affiche le parcours qui determine si le graph est cyclique, affiche un message si il l'est ou non"""
        if not self.annim : 
            self.annim = True
            cycle = self.laby.getgraph().MatriceEstCyclique(self.laby.getdebut())
            self.annimer(cycle[1],canvas,ax,fig1,h,l,False)
            if cycle[0]:
                messagebox.showinfo('Détéction de cycle', 'le graphe du labyrinthe est cyclique')
            else :
                messagebox.showinfo('Détéction de cycle', 'le graphe du labyrinthe est acyclique')
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def solution_parcours_largeur(self,canvas,ax,fig1,h: int,l: int):
        """Affiche la solution qui utilise le parcours en largeur"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().solution(self.laby.getfin(),self.laby.getgraph().parcours_largeur_dict(self.laby.getdebut()))
            self.annimer(parcours,canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def solution_parcours_largeur_rec(self,canvas,ax,fig1,h: int,l: int):
        """Affiche la solution qui utilise le parcours en largeur recursif"""
        try :
            if not self.annim : 
                self.annim = True
                parcours = self.laby.getgraph().solution(self.laby.getfin(),self.laby.getgraph().parcours_largeur_dict_rec(self.laby.getdebut()))
                
                self.annimer(parcours,canvas,ax,fig1,h,l)
            else :
                messagebox.showinfo('Annimation','un annimation est déja en cours')
        except RecursionError : #si il y'a trop d'appel recursif ne rien afficher
            self.annim = False
            messagebox.showerror('Recursivité',"Un labyrinthe de cette taille ne peut pas se resoudre recursivement (trop d'appel recursif)")

    def solution_parcours_profondeur(self,canvas,ax,fig1,h: int,l: int):
        """Affiche la solution qui utilise le parcours en profondeur"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().solution(self.laby.getfin(),self.laby.getgraph().parcours_profondeur_dict_bis(self.laby.getdebut()))
            self.annimer(parcours,canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def solution_parcours_profondeur_rec(self,canvas,ax,fig1,h: int,l: int):
        """Affiche la solution qui utilise le parcours en profondeur recursif"""
        try :
            if not self.annim : 
                self.annim = True
                parcours = self.laby.getgraph().solution(self.laby.getfin(),self.laby.getgraph().parcours_profondeur_dict_rec(self.laby.getdebut()))
                self.annimer(parcours,canvas,ax,fig1,h,l)
            else :
                messagebox.showinfo('Annimation','un annimation est déja en cours')
        except RecursionError : #si il y'a trop d'appel recursif ne rien afficher
            self.annim = False
            messagebox.showerror('Recursivité',"Un labyrinthe de cette taille ne peut pas se resoudre recursivement (trop d'appel recursif)")

    def laby_dijkstra_alea(self,canvas,ax,fig1,h: int,l: int):
        """Affiche le parcours de l'algorithme de dijkstra utilisant des poids aléatoire"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().dijkstra(self.laby.getdebut(),self.laby.getfin())
            self.annimer(parcours[1],canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

    def laby_dijkstra_poid(self,canvas,ax,fig1,h: int,l: int):
        """Affiche le parcours de l'algorithme de dijkstra utilisant des poids de 1 a chaque arrete"""
        if not self.annim : 
            self.annim = True
            parcours = self.laby.getgraph().dijkstra(self.laby.getdebut(),self.laby.getfin(),False)

            self.annimer(parcours[1],canvas,ax,fig1,h,l)
        else :
            messagebox.showinfo('Annimation','un annimation est déja en cours')

def plotcases(ax, laby: Labyrinthe, color: str,h: int,l: int,p: bool ):
    """fonction qui affiche le labyrinthe dans la fenètre matplotlib"""
    for elm in laby.__dict__(): #pour tout les lément du labyrinthe
        x,y = nomx(elm),nomy(elm) #on detarmine les cooerdonnée de la case avec le nom de celle ci
        if not laby.chemin_existe(elm,f'{x+1},{y}'): #si le chemin n'existe pas entre la case et la case de droite 
            ax.plot([x+0.5, x+0.5],[y+0.5, y-0.5],color=color) #afficher le mur associé
        elif p and laby.getgraph().get_poid(elm,f'{x+1},{y}') != None: #si le chemin existe entre la case et la case de droite afficher la pondération associée si la pondération est activée
            ax.text(x+0.5,y,color=color,s=str(int(laby.getgraph().get_poid(elm,f'{x+1},{y}'))),size=6,horizontalalignment='center')
        if not laby.chemin_existe(elm,f'{x},{y+1}'): #si le chemin n'existe pas entre la case et la case du haut 
            ax.plot([x-0.5,x+0.5],[y+0.5, y+0.5],color=color) #afficher le mur associé
        elif p and laby.getgraph().get_poid(elm,f'{x},{y+1}') != None: #si le chemin existe entre la case et la case de droite afficher la pondération associée si la pondération est activée
            ax.text(x,y+0.5,color=color,s=str(int(laby.getgraph().get_poid(elm,f'{x},{y+1}'))),size=6,horizontalalignment='center')
    ax.plot([-0.5,-0.5],[-0.5, h-0.5],color=color) #affichage des deux bordures manquantes
    ax.plot([-0.5,l-0.5],[-0.5, -0.5],color=color)
    d,f = laby.getdebut(), laby.getfin() #on defini le debut et la fin du labyrinthe
    try :
        if h <= 30 and l <= 30 : #si le labyrinthe est plus peti que 30x30
            if ctk.get_appearance_mode() == "Light": #on chosit les images en fonction de la couleur du thème
                file1 = 'images\\bentree.png'
                file2 = 'images\\bflag.png'
            if ctk.get_appearance_mode() == "Dark" :
                file1 = 'images\entree.png'
                file2 = 'images\\flag.png'
            z1 = 0.772152 - 0.112648*np.log(18.0365*max(h,l)- 12.8067) #on calcule la taille relative de chaque images en fonction de la taille du labyrinthe, la formule a été trouvé par tatonement
            z2 = 0.47352- 0.0704762*np.log(14.5187*max(h,l)- 10.1672) #de meme pour l'image de fin
            if z1 <= 0.09 or z2 <= 0.05 : #si l'images est trop petite on redéfini les valeurs a avoire
                z1 = 0.09
                z2 = 0.05
                file1 = 'images\\rentree.png'
                file2 = 'images\\rflag.png'
            plot_image(nomx(d), nomy(d),ax,file1,z1) #on affiche les images
            plot_image(nomx(f), nomy(f),ax,file2,z2)
        else : #sinon on affiche simplement deux points, un vert pout l'entrée, un rouge pour la sortie
            ax.plot(nomx(d), nomy(d), marker="o", markersize=5, color="green")
            ax.plot(nomx(f), nomy(f), marker="o", markersize=5, color="red")
    except : #si le code echoue on affiche une errer et on affiche simplement deux points, un vert pout l'entrée, un rouge pour la sortie
        messagebox.showerror('Erreur Fichiers', "Les Fichiers du programme on été modifié, les images ne charge pas, le depart sera donc noté par un point vert, et l'arrivée par un point rouge") 
        ax.plot(nomx(d), nomy(d), marker="o", markersize=5, color="green")
        ax.plot(nomx(f), nomy(f), marker="o", markersize=5, color="red")
       
    



if __name__ == "__main__":
    try :
        f=open('preférences.config') #on lit le fichier des préférences
        lines=f.readlines()
        theme = lines[0].split(',')[0]
        color = lines[0].split(',')[1]
        taille = lines[0].split(',')[2] #on verifie que ce sont des bonnes valeurs
        if theme in ["light","dark","system"] and color in ["blue","dark-blue","green"] and taille in ['1920x1080','1080x720','1020x760','855x620']:
            theme = lines[0].split(',')[0]
            color = lines[0].split(',')[1]
            taille = lines[0].split(',')[2]
        else :  #sinon on affiche une erreur et on lance le programme avec des valeurs par défault
            messagebox.showerror('Erreur Préférences', 'Le programme ce lance sur les valeurs de préférence par défault car il ne peut pas correctement lire le fichier config') 
            theme = "dark"
            color = "blue"
            taille = "1080x720"
            with open('preférences.config','w') as file:
                file.write("dark,blue,1080x720,None,None,None,False")
    except: #si le code echoue on lance le programme avec des valeurs par défault
        theme = 'dark'
        color = 'blue'
        taille = "1080x720"
    ctk.set_appearance_mode(theme) #on change le thème de l'application
    ctk.set_default_color_theme(color)  #on change la couleur du thème de l'application
    root = Windows(theme,color,taille) #on lance l'application
    root.mainloop() #on lance la boucle tkinter