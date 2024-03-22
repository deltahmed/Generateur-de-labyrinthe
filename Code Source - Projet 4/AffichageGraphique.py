from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image,ImageTk

from typing import List,Union,Tuple,Callable

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt

class BarreOutils(NavigationToolbar2Tk): #Réecriture de la class NavgationToolbar2Tk, qui permet de choisir les outils disponibles dans la barre de navigation de matplotlib
    '''Réecriture de la class NavgationToolbar2Tk, qui permet de choisir les outils disponibles dans la barre de navigation de matplotlib'''
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] in ('Home','Back','Forward', 'Pan', 'Zoom', 'Save')]

def button(master, text: str, command: Callable) : #creer un bouton sur la fenetre ou la frame master
    '''Prend une frame ou une fenetre master, un texte et une commande en paramètre et creer un boutton'''
    b = ctk.CTkButton(master=master, text=text, command=command,font=('Arial', 18)) # bouton de la bibliothèque customtkinter
    b.pack(side=tk.TOP, padx=20,pady=10,) #pack avec 10 de marge y et 20 de marge x

def button_left(master, text: str, command: Callable) : #creer un bouton sur la gauche sur la fenetre ou la frame master
    '''Prend une frame ou une fenetre, un texte et une commande en paramètre et creer un boutton qui sera pack a gauche'''
    b = ctk.CTkButton(master=master, text=text, command=command,font=('Arial', 18)) # bouton de la bibliothèque customtkinter
    b.pack(side=tk.LEFT, padx=2,pady=10,) #pack avec 10 de marge y et 2 de marge x
    return b #on retourne le bouton en question pour pouvoir le manipuler plus tard

def multiple_button(master,num: int,listtexts: List[str], listcmd: List[Callable]): #creer plusieurs bouttons allignée
    '''Prend une frame ou une fenetre master,un nombre n de boutton, une liste de n textes et une liste de n commandes en paramètre et creer plusieurs boutton alignée sur master'''
    frame = ctk.CTkFrame(master, fg_color="transparent") # on inistialise une frame
    l = []
    for i in range(num): #pour chaque element de la liste creer des bouttons a gauche de frame
        x = button_left(frame,text=listtexts[i],command=listcmd[i])
        l.append(x)
    frame.pack()
    return l #on retourne tout les boutons dans une liste pour pouvoir les manipuler plus tard

def titre(master,text: str) : #affiche un titre sur la fenetre
    '''Prend une frame ou une fenetre master ainsi qu'un texte en paramètre et creer un titre sur la fenètre'''
    text_var = tk.StringVar(value=text)
    label = ctk.CTkLabel(master=master,textvariable=text_var,font=('Arial', 40)) #texte
    label.pack(padx=20,pady=10) #pack avec 10 de marge y et 20 de marge x

def text(master,text: str, taille=18) : # affiche un texte sur la fenetre
    '''Prend une frame ou une fenetre master,un texte et une taille de police en paramètre et creer un texte sur la fenètre'''
    text_var = tk.StringVar(value=text)
    label = ctk.CTkLabel(master=master,textvariable=text_var,font=('Arial', taille)) #texte de taille taille
    label.pack(padx=5,pady=5) #pack avec 5 de marge y et 5 de marge x
    return label # on retourne le texte pour pouvoir le manipuler plus tard

def champ(master) : # champs de texte
    '''prend en paramètre une fenetre ou une frame et renvoie un champ de texte'''
    return ctk.CTkEntry(master) # entry de la bibliothèque customtkinter

def selection(master,Titre: str,values: list, default: str):
    '''prend en paramètre une fenetre ou une frame, un titre, une liste de valeurs et une valeur par default et renvoie un boite de séléction'''
    combobox_var = ctk.StringVar(value=default)  # valeur initials
    frame = ctk.CTkFrame(master, fg_color="transparent") #on creer une nouvelle frame
    text_var = tk.StringVar(value=Titre) 
    label = ctk.CTkLabel(master=frame,textvariable=text_var,font=('Arial', 18))
    label.pack(padx=5,pady=5,side= tk.LEFT) 
    select = ctk.CTkComboBox(master=frame,values=values,state="readonly", variable=combobox_var) #combobox de etkinter
    select.pack(padx=20, pady=10, side = tk.LEFT)
    frame.pack()
    return select #on retourne la boite de selection pour pouvoir la manipuler plus tard

def choosecolors(master,Titre:str, command: Callable): 
    """prend un titre une fenètre et une commande en paramètre et affiche un bouton pour choisir la couleur"""
    try: 
        frame = ctk.CTkFrame(master, fg_color="transparent") #creation d'une nouvelle frame
        text_var = tk.StringVar(value=Titre)
        label = ctk.CTkLabel(master=frame,textvariable=text_var,font=('Arial', 18)) # création du texte 
        label.pack(padx=5,pady=5,side= tk.LEFT) 
        img = Image.open('images\colorw.png')  # on ouvre l'icone
        photo_image = ctk.CTkImage(light_image=img,dark_image=img,size=(15,15)) 
        b = ctk.CTkButton(master=frame, command=command,text='', image=photo_image, width=16) #on crée un boutton avec cette icone
        b.pack(side= tk.LEFT) 
        frame.pack() #on affiche le tout
    except : # si le programme echoue renvoyer une erreur
        messagebox.showerror('Erreur',"Le programme a rencontrée un problème dans l'affichage des boutons")

def checkbox(master,Titre:str, command, on, off, defaultvar):
    """prend un titre une fenètre et une commande, une valeur quand la case est coché et une autre quand elle ne l'est pas ainsi qu'une
    valeur par defaut en paramètre et afficheune case a cocher"""
    frame = ctk.CTkFrame(master, fg_color="transparent") #creation d'une nouvelle frame
    check_var = tk.BooleanVar(value=defaultvar)
    checkbox = ctk.CTkCheckBox(master=frame, text=Titre, command=command,variable=check_var, onvalue=on, offvalue=off) #creation de la checkbox
    checkbox.pack(side= tk.LEFT)
    frame.pack() #affichage du tout
    return checkbox # on retourne la check box pour pouvoir la manipuler plus tard

def menubox(master, Titre: str, desc: str, *args: Tuple[str,Callable]):
    """Prend en paramètre une fenètre, un Titre, un déscription, ainsi que des Tuples Titre/commandes qui permet de creer un menu deroulant"""
    frame = ctk.CTkScrollableFrame(master=master,border_color=('#000000','#FFFFFF'),height=450,width=300,border_width=4,corner_radius=20) #on creer une frame avec une barre deroulante
    if Titre != None: #on crée le Titre si il est différent de None
        text(frame,Titre,25)
    if desc != None: #on crée la description si il est différent de None
        text(frame,desc,12)
    for texte,command in args: # pour chaque texte et chaque commande si elle n'est pas egal a None on crée le bouton approprié
        if command != None :
            b = ctk.CTkButton(master=frame, text=texte, command=command,font=('Arial', 18)) # bouton de la bibliothèque customtkinter
            b.pack(side=tk.TOP, padx=5,pady=5,) #pack avec 10 de marge y et 20 de marge x
        else : # sinon on ecrit juste un texte
            text(frame,texte,18)
    frame.pack() #on affiche le menu
    frame.place(relx=-1, rely=-1, anchor='ne') #on place le menu en dehors de la fenètre
    return frame #on retourne le menu pour pouvoire le manipuler plus tard

def toolbarmatplotlib(canvas,master) -> BarreOutils: 
    """creer une barre de navigation matplotlib"""
    imglist = []
    if ctk.get_appearance_mode() == 'Dark' : #on défini les images a afficher et la couleur du fond en fonction de thème de l'application 
        color = '#2B2B2B'
        imgfileliste = ["images\\home.png","images\\gauche.png","images\\droite.png","images\\nav.png","images\\zoom.png","images\\save.png"]
    if ctk.get_appearance_mode() == 'Light' :
        color = '#DBDBDB'
        imgfileliste = ["images\\bhome.png","images\\bgauche.png","images\\bdroite.png","images\\bnav.png","images\\bzoom.png","images\\bsave.png"]
    try : 
        for files in imgfileliste : #pour chaque images on creer des objet de type Tkimages
            img = Image.open(files)
            if files in ["images\\bgauche.png","images\\bdroite.png","images\\gauche.png","images\\droite.png"] :
                img = img.resize((24,24), Image.Resampling.LANCZOS)
            imgphoto = ImageTk.PhotoImage(img)
            imglist.append(imgphoto)
        toolbar = BarreOutils(canvas, master, pack_toolbar=False) #on creer notre barre d'outils grace a la class BarreOutils
        toolbar.config(background=color) #on configure son fond 
        imageindex = 0
        for w in toolbar.winfo_children(): #pour tout les élement de la barre d'outils on change les images que si ce sont des boutton ou des checkbox
            if w.winfo_class() == 'Button' or w.winfo_class() == 'Checkbutton':
                w.config(background=color,relief=tk.FLAT,highlightcolor='black',image=imglist[imageindex])
                w.image = imglist[imageindex]
                imageindex += 1
            else :
                w.config(background=color,relief=tk.FLAT) #sinon pour les autres element on défini la couleur de fond ainsi que le relief (pour les labels)
    except: # si le code echoue envoyer une erreur et lancer le programme quand meme avec des valeurs par default
        messagebox.showerror('Erreur Fichiers', 'Les fichier du programme on été modifiés, demarage sans graphiques')
        toolbar = BarreOutils(canvas, master, pack_toolbar=False)
        toolbar.config(background=color)
    toolbar.update() 
    return toolbar # on retourne la barre d'outils que l'on viens de creer

def plot_image(x: Union[int,float],y: Union[int,float],ax,path: str,zoom: Union[int,float]=1): 
    ab = AnnotationBbox(OffsetImage(plt.imread(path, format="png"), zoom=zoom), (x, y), frameon=False,) #on creer une annotation dans la quel on met l'image 
    ax.add_artist(ab) #on l'ajoute aux axes matplotlib
