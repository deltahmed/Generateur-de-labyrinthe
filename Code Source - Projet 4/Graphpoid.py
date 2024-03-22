from __future__ import annotations
import math
from random import randint
from typing import List,Union,Tuple
from PileFile import *
from GraphL import *


class Graph_Weighted(Graph):
    """Class enfant de la class Graph qui permet la création d'un graph pondérée"""
    def __init__(self, *args: str): #on initialise la class comme la class graph
        self.poids = []
        self.graph = {}
        for arg in args:
            self.add_sommet(arg) #on utilise la methode parent add_sommet pour chaque argument de la class
    
    def from_dict_list(self,listesommet: List[str] ,listpoids: List[Tuple[str,str,Union[int,float]]]): 
        """méthode qui permet de creer un graph a partir d'une liste de sommet et d'une liste de tuple contenant les arretes ainsi que leur poids"""
        for element in listesommet :
            self.add_sommet(element) #on utilise la methode parent add_sommet pour chaque élment de la liste
        for element in listpoids :
            self.add_weighted_arrete(element[0],element[1],element[2]) #on utilise la methode add_weighted_arrete pour chaque élment de la liste

    def getlistpoids(self) -> List[Tuple[str,str,Union[int,float]]]:
        """retourn la liste de tuple contenant les arretes ainsi que leur poids"""
        return self.poids

    def add_weighted_arrete(self, nom1: str, nom2: str, poids: Union[int,float]=1.0):
        """ Méthode qui ajoute une arrete dans le graph"""
        self.add_arrete(nom1, nom2) #on utilise la methode parent add_arrete pour chaque élment de la liste
        self.poids.append((nom1,nom2,float(poids))) # on ajoute a la liste des poids le poids associée
    
    def del_weighted_arrete(self,nom1: str, nom2: str):
        """ Méthode qui supprime une arrete dans le graph"""
        for elem in self.poids : #on supprime dans la liste des poids le tuple correspondant
            if nom1 and nom2 in elem :
                self.poids.remove(elem)
        self.del_arrete(nom1, nom2) #on utilise la methode parent del_arrete pour chaque élment de la liste
    
    def re_ponderation_aleatoire(self,rangepoid: Union[int,float]): 
        """permet une repondération aléatoire du graph"""
        l = []
        for elem in self.poids : 
            elem = (elem[0],elem[1],float(randint(0,rangepoid))) #pour tout les élément de la liste des poids on change le poid par une valeur aléatoire entre 0 et la fin de l'interval donnée
            l.append(elem)
        self.poids = l
    
    def get_poid(self, sommet1: str, sommet2: str, fromself: bool = True, listpoids: List[Tuple[str,str,Union[int,float]]]=[]):
        """permet de recuperer le poid d'un sommet du graph depuis celui ci ou depuis une liste externe au graph"""
        if fromself :
            for elem in self.poids :
                if sommet1 and sommet2 in elem : # si l'arrete et dans la liste de poids alors on retourne le poid
                    return elem[2]
            
        else :
            for elem in listpoids :
                if sommet1 and sommet2 in elem : # si l'arrete et dans la liste de poids alors on retourne le poid
                    return elem[2]

        
    def get_dictgraph(self,pondere: bool =True) -> dict:
        """transphorme le graph en un dictionnaire de dictionnaire"""
        dictgraph = dict()
        for elm in self.graph.keys(): #pour tout les elment dans le graph
            d = dict()
            for voisin in self.voisin(elm) : #on creer un dictionaire de la liaison contenant un poid si il est pondérée sinon un poid de 1
                if pondere:
                    d[voisin] = self.get_poid(elm,voisin)
                else :
                    d[voisin] = 1.0
            dictgraph[elm] = d
        return dictgraph

    def get_dictgraph_nx(self,pondere: bool=True) -> dict:
        """transphorme le graph en un dictionnaire de dictionnaire de dictionnaire pour les convertions networkx"""
        dictgraph = dict()
        for elm in self.graph.keys(): #pour tout les elment dans le graph
            d = dict()
            for voisin in self.voisin(elm) : #on creer un dictionaire de la liaison contenant un poid si il est pondérée sinon un poid de 1
                if pondere:
                    d[voisin] = {"weight":self.get_poid(elm,voisin)} #on ajoute un autre dictionnaire contenant l'attribut weight
                else :
                    d[voisin] = {"weight":1.0}
            dictgraph[elm] = d
        return dictgraph

    def dijkstra(self,debut: str,fin: str, pondere: bool =True) -> Tuple[Union[math.inf,float],List[str]]:
        """ algorithme du plus cours chemins entre deux sommet, avec un poid defini ou un poid de 1 par noeud (argument pondere)"""
        if pondere :
            dictgraph = self.get_dictgraph() #on transforme le graph en dictionaire de dictionaire pour faciliter la manipulation des donnée
        else :
            dictgraph = self.get_dictgraph(False)#on transforme le graph en dictionaire de dictionaire avec un poid de 1 par noeud
        Nonvisite = dictgraph #on initialise tout les sommet comme non visité
        distance_min = {} # on initialise un dictionnaire contenant les distance minimum
        route = [] # une liste qui contiendra la route la plus courte 
        chemin = {} # un dictionnaire qui contiendera les chemins les plus cours pour aller d'un sommet a un autre

        for Noeud in Nonvisite: # pour tout les noeud du graph
            distance_min[Noeud] = math.inf #on initialise la distance minimun a l'infinie
        distance_min[debut] = 0 #on initialise la distance du noeud de départ a 0

        while Nonvisite: # tant que Nonviste n'est pas vide
            min_Noeud = None # on donne comme valeur a min_Noeud None
            for courant in Nonvisite: #pour chaque noeud dans Nonvisite
                if min_Noeud is None: # min_Noeud est egal a None
                    min_Noeud = courant # on donne comme valeur a min Noeud le Noeud courant
                elif distance_min[min_Noeud] > distance_min[courant]: #sinon si la distance minimal de min_Noeud est superieur a la distance minial du Noeud courant
                    min_Noeud = courant # on donne comme valeur a min Noeud le Noeud courant
            for Noeud, Valeur in Nonvisite[min_Noeud].items(): #pour chaque Noeud et chaque valeur dans le dictionnaire associée a min_Noeud dans Nonvisite
                if Valeur + distance_min[min_Noeud] < distance_min[Noeud]: #si la valeur + la distance minimal de min_Noeud est inferieur a la distance minimal du Noeud
                    distance_min[Noeud] = Valeur + distance_min[min_Noeud] #on change la valeur de la distance minimal du Noeud avec cette somme
                    chemin[Noeud] = min_Noeud #on donne pour chemin a Noeud min_Noeud soit le Noeud avant lui dans le parcoursdu graph
            Nonvisite.pop(min_Noeud) #on enlève un élément de Nonvisite
        Noeud = fin #on donne comme valeur a Noeud le sommet final

        while Noeud != debut: # tant que Noeud n'est pas egal au Noeud de départ
            try: 
                route.insert(0, Noeud) #on insert dans la route parcourue devant l'indice 0 le Noeud
                Noeud = chemin[Noeud] #on change la valeur de Noeud avec le chemin correspondant a Noeud (le Noeud avant lui dans le parcours)
            except Exception: # si le code echoue
                return math.inf,route # on retourne l'infinie ainsi que la route parcourue
        route.insert(0, debut) # on insert le premier Noeud 

        if distance_min[fin] != math.inf: # si la distance minimal du noeud final n'est pas egal a l'infinie 
            return distance_min[fin],route #alors on retourne la distance minimal ansi que la route parcourue
        
        
if __name__=='__main__': # quelques teste de la class Graph_Weighted
    print('Graph a poids -----------------------------------------------------------------------------------')
    G = Graph_Weighted('a','b','c','d','e','f','g','h')
    G.add_weighted_arrete('a','b',5)
    G.add_weighted_arrete('a','c')
    G.add_weighted_arrete('b','d',2)
    G.add_weighted_arrete('b','e',3)
    G.add_weighted_arrete('c','d')
    G.add_weighted_arrete('d','e')
    G.add_weighted_arrete('e','f')
    G.add_weighted_arrete('e','g')
    G.add_weighted_arrete('f','g')
    G.add_weighted_arrete('g','h')
    print(G.graph)
    print(G.poids)
    print(G.parcours_largeur_dict_rec('a'))
    print(G.get_dictgraph())
    print(G.dijkstra('a','f',False))
    print(G.dijkstra('a','f'))
