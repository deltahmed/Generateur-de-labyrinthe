from __future__ import annotations
import networkx as nx
import matplotlib.pyplot as plt
from random import randint,choice
from Graphpoid import *
from typing import Union,Tuple,Callable
from PileFile import *
from math import sqrt
import time
class Labyrinthe:
    def __init__(self, hauteur, longueur, gen=True):
        """
        Créer un labyrinthe de taille hauteur x longueur, en le générant ou non (pour future importation de labyrinthe)
        """
        self.hauteur , self.longueur = hauteur, longueur
        self.pos , self.grillevide, self.visites = self.construire_grille()
        if gen :
            self.creer_labyrinthe()

    def construire_grille(self) -> Tuple[dict, Graph_Weighted, dict]:
        """
        Cette méthode crée une grille vide de taille hauteur x longueur. Elle renvoie :
        - pos : un dictionnaire où les clés sont les coordonnées de chaque point dans la grille (x,y) pour l'affichage plus tard avec networkx.
        - grillevide : un graph de  hauteur x longueur sans arretes.
        - visites : un dictionnaire où les clés sont les noeud et ou toute les valeurs sont initialisé a False.
        """
        grillevide = Graph_Weighted()
        pos = dict()
        visites = dict()
        for i in range(self.longueur):
            for j in range(self.hauteur):
                grillevide.add_sommet(f'{i},{j}')
                pos[f'{i},{j}'] = (i,j)
                visites[f'{i},{j}'] = False
        return pos,grillevide,visites

    def  __dict__(self) -> dict:
        """
        Renvoie la représentation en dictionnaire du Graph du labyrinthe.
        """
        return self.grillevide.__dict__()
    def __repr__(self):
        """renvoie le string correspondant au labyrinthe"""
        return f"Labyrithe({self.grillevide.__dict__()})"

    def __len__(self) -> int :
        """Renvoie le nombre de sommets du Graph"""
        return len(self.grillevide)

    def __getitem__(self, nom: str) -> list[str]:
        """renvoie les sommet adjacent a un sommet"""
        return self.grillevide.__getitem__(nom)

    def __contains__(self,x):
        """Renvoie True si le sommet donné est dans le labyrinthe, et False sinon"""
        return x in self.grillevide

    def getgraph(self) -> Graph_Weighted:
        """renvoie le graph du labyrinthe"""
        return self.grillevide

    def graph_poids_aleatoire(self,rangepoid: int):
        """Attribue un poids aléatoire entre 0 et rangepoid à chaque arête du graphe"""
        self.grillevide.re_ponderation_aleatoire(rangepoid)

    def getpos(self):
        """retourne la position de chaque noeud"""
        return self.pos

    def nomisvalid(self, nom: str) -> bool :
        """retourne vrai si le noeud existe dans le labyrinthe"""
        return nom in self.visites

    def visitee(self,nom: str) -> bool:
        """retourne vrai si le noeud a déja été visité"""
        return self.visites[nom] == True

    def voisins(self, nom: str) -> list[str] :
        """retourne les voisins (haut/bas/gauche/droite) existant dans le labyrinthe"""
        x,y = nomx(nom),nomy(nom)
        valid = []
        voisins = [f'{x+1},{y}',f'{x-1},{y}',f'{x},{y+1}',f'{x},{y-1}']
        for voisin in voisins :
            if self.nomisvalid(voisin) :
                valid.append(voisin)
        return valid

    def voisin_nonvisite(self, nom: str) -> list[str]:
        """retourne la liste des voisins qui n'ont pas encore été visité"""
        l = []
        for voisin in self.voisins(nom):
            if not self.visitee(voisin) :
                l.append(voisin)
        return l

    def voisin_dispo(self,nom: str) -> bool :
        """retrourne vrai si des voisin pas encore visité son disponibles"""
        if self.voisin_nonvisite(nom) == [] :
            return False
        return True

    def tout_est_visite(self) -> bool :
        """retorune vrai si toute les cases du labyrinthes on déja été visité"""
        for sommet in self.visites:
            if self.visites[sommet] == False :
                return False
        return True

    def chemin_existe(self, nom1: str, nom2: str) -> bool:
        """retourne vrai si un chemin existe entre deux cases"""
        return self.grillevide.arrete_existe(nom1,nom2)
    
    def creer_labyrinthe(self):
        """Creer le labyrinthe en question, avec un début une fin"""
        P = Pile() #intitialisation d'une pile vide
        Noeud = f'{randint(0,self.longueur-1)},{randint(0,self.hauteur-1)}' #On nchoisit aléatoirement un Noeud de départ
        V = self.tout_est_visite() 
        while not V: #tant que toute les cases n'ont pas été visité
            P.empiler(Noeud) #On empile le noeud dans la pile P
            self.visites[Noeud] = True #on marque ce Noeud comme visité
            if self.voisin_dispo(Noeud): # si un voisin est disponible alors 
                adjacent = choice(self.voisin_nonvisite(Noeud)) #on choisit un voisin adjacent aléatoirement
            else : # aucun voisin n'est disponible alors 
                n = self.voisin_nonvisite(Noeud) 
                while len(n) == 0 and not self.tout_est_visite(): #tant qu'ils n'a pas de voisin a visiter et qu'il reste des cases non visité 
                    Noeud = P.depiler() #on dépile la pile jusqu'a trouver un Noeud avec encore des voisins non visité
                    n = self.voisin_nonvisite(Noeud)
                if len(n) != 0 : #on choisit donc un voisin adjacent aléatoirement
                    adjacent = choice(self.voisin_nonvisite(Noeud))
            P.empiler(adjacent)#on empile le noeud de la case adjacente
            if Noeud != adjacent : #si le Noeud est différent de sont adjacent
                self.grillevide.add_weighted_arrete(Noeud,adjacent) #on ajoute une arrete au graphe
            Noeud = adjacent #on change la valeur du Noeud avec son adjacent
            V = self.tout_est_visite()
        if self.longueur > 7 and self.hauteur > 7 and self.longueur < 150 and self.hauteur < 150: #si la longeur et la hauteur sont entre 7 et 150 
            for _ in range(randint(4,self.longueur*self.hauteur//8)): 
                n  = f'{randint(0,self.longueur-1)},{randint(0,self.hauteur-1)}'  #on choisi un noeud aléatoirement un nombre de fois aleatoire 
                if len(self.voisins(n)) > 2 : # si il y'a plus de 2 voisins 
                    for _ in range(randint(2,len(self.voisins(n)))): #on choisi aléatoirement un nombre de voisin a relier 
                        adj = choice(self.voisins(n))
                        self.grillevide.add_weighted_arrete(n,adj) # on relie les deux noeud, cela permet de ne pas avoir q'une seul solution au labyrinthe 
        debutfin = choice([(f'{0},{0}',f'{self.longueur-1},{self.hauteur-1}'), #on choisit aléatoirement deux coin opposée du labyrinthe
                        (f'{self.longueur-1},{self.hauteur-1}',f'{0},{0}'),
                        (f'{0},{self.hauteur-1}',f'{self.longueur-1},{0}'),
                        (f'{self.longueur-1},{0}',f'{0},{self.hauteur-1}')])
        self.debut = debutfin[0] #on défini le début
        self.fin = debutfin[1] #on défini la fin
        self.casecoin = debutfin[0] #on défini le coin du  début pour l'affichage graphique
        if self.longueur > 8 and self.hauteur > 8: #si la longeure et la hauteur sont plus grande que 8 cases, on choisi une range grace a une formule optenue par tatonement
            rangernum = int(round(sqrt(self.longueur * self.hauteur *0.09))) #le début et la fin du labyrinthe sont choisit aleatoirement dans une zone  definie par la formule
            if debutfin == (f'{0},{0}',f'{self.longueur-1},{self.hauteur-1}') : # on definie cela pour tout les cas possibles
                self.debut = f'{nomx(self.debut)+randint(1,rangernum)-1},{nomy(self.debut)+randint(1,rangernum)-1}'
                self.fin = f'{nomx(self.fin)-randint(1,rangernum)+1},{nomy(self.fin)-randint(1,rangernum)+1}'
            if debutfin == (f'{self.longueur-1},{self.hauteur-1}',f'{0},{0}') :
                self.debut = f'{nomx(self.debut)-randint(1,rangernum)+1},{nomy(self.debut)-randint(1,rangernum)+1}'
                self.fin = f'{nomx(self.fin)+randint(1,rangernum)-1},{nomy(self.fin)+randint(1,rangernum)-1}'
            if debutfin == (f'{0},{self.hauteur-1}',f'{self.longueur-1},{0}') :
                self.debut = f'{nomx(self.debut)+randint(1,rangernum)-1},{nomy(self.debut)-randint(1,rangernum)+1}'
                self.fin = f'{nomx(self.fin)-randint(1,rangernum)+1},{nomy(self.fin)+randint(1,rangernum)-1}'
            if debutfin == (f'{self.longueur-1},{1}',f'{1},{self.hauteur-1}') :
                self.debut = f'{nomx(self.debut)-randint(1,rangernum)+1},{nomy(self.debut)+randint(1,rangernum)-1}'
                self.fin = f'{nomx(self.fin)+randint(1,rangernum)-1},{nomy(self.fin)-randint(1,rangernum)+1}'

    def getdebut(self) -> str:
        """retourne le debut du labyrinthe"""
        return self.debut
    def getfin(self) -> str:
        """retourne la fin du labyrinthe"""
        return self.fin
    def getcoin(self) -> str:
        """retourne le coin du debut du labyrinthe"""
        return self.casecoin 

    def affichergraph(self):
        """affiche le graphe du labyrinthe (sans pondération)"""
        graphnx = nx.Graph(self.grillevide.__dict__())
        nx.draw(graphnx,pos=self.pos)
        plt.show()
            

def nomx(nom: str) -> int:
    """retourne l'abssice x dans le nom d'un sommet de type x,y"""
    return int(nom.split(',')[0])

def nomy(nom: str) -> int:
    """retourne l'ordonnée y dans le nom d'un sommet de type x,y"""
    return int(nom.split(',')[1])

def nomxy(nom: str) -> Tuple[int,int]:
    """retourne x et y dans le nom d'un sommet de type x,y"""
    return nomx(nom),nomy(nom)



if __name__ == '__main__': #on teste les différentes méthodes ainsi que leur efficacité
    for i in range(10,100,20) :
        start_time = time.time()
        laby = Labyrinthe(i,i)
        print("--------------------------------------------------------------------------------------")
        print(f"--- génération d'un labyrinthe de {i}x{i} en {time.time() - start_time } secondes ---")
        start_time = time.time()
        solution = laby.getgraph().solution(laby.getdebut(),laby.getgraph().parcours_largeur_dict(laby.getfin()))
        print(f"--- solution parcours en largeur, parcours de {len(solution)} cases en {time.time() - start_time } secondes ---")
        try : 
            start_time = time.time()
            solution = laby.getgraph().solution(laby.getdebut(),laby.getgraph().parcours_largeur_dict_rec(laby.getfin()))
            print(f"--- solution parcours en largeur rec, parcours de {len(solution)} cases en {time.time() - start_time } secondes ---")
        except RecursionError:
            print("--- solution parcours en largeur rec : trop d'appel recursif ---")
        start_time = time.time()
        solution = laby.getgraph().solution(laby.getdebut(),laby.getgraph().parcours_profondeur_dict_bis(laby.getfin()))
        print(f"--- solution parcours en profondeur, parcours de {len(solution)} cases en {time.time() - start_time } secondes ---")
        try :
            start_time = time.time()
            solution = laby.getgraph().solution(laby.getdebut(),laby.getgraph().parcours_profondeur_dict_rec(laby.getfin()))
            print(f"--- solution parcours en profondeur rec, parcours de {len(solution)} cases en {time.time() - start_time } secondes ---")
        except RecursionError:
            print("--- solution parcours en profondeur rec : trop d'appel recursif ---")
