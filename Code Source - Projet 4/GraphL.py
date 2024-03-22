#import des bibliothèque nécessaire 
from __future__ import annotations
from functools import reduce
from random import choice
from typing import Union,Tuple
from PileFile import *

#class Graph et Matrice crée pour l'activité sur les graph, ce sont quasiment les meme fontions que dans le cours 

class Matrice:
    def __init__(self, listepoints: list[str] , M: list[list] ):
        """Matrice d'adjacence"""
        self.n = len(listepoints)
        self.liste = listepoints
        self.M = M
    def __repr__(self):
        """affichage de la matrice lors d'un print"""
        string = ''.join(map(lambda x: x + '  ', self.liste))
        if len(self.M) > 1 :
            s=f'Matrice(   {string}\n'
            for i in range(0,len(self.M)-1):
                s += f"        {self.liste[i]} {self.M[i]}\n"
            return s + f"        {self.liste[-1]} {self.M[-1]} )"
        else :
            return f'Matrice({self.M[0]})'
    def __len__(self) -> int :
        """taille de la matrice"""
        return self.n
    def __getitem__(self,i) -> list[int]:
        """retourne une ligne de la matrice"""
        return self.M[i]
    
    def get_list(self) -> list[list[int]]:
        """retourne la liste de lise de la matrice"""
        return self.M
    def get_graph(self) -> Graph :
        """retourne le graph correspondant a la matrice d'adjacence"""
        Final = Graph(*self.liste)
        for i in range(self.n):
            for j in range(self.n):
                if self.M[i][j]==1 :
                    Final.add_arrete(self.liste[i],self.liste[j])
        return Final

    def  __dict__(self) -> dict: 
        """retourne le dictionnaire correspondant au graph correspondant a la matrice d'adjacence"""
        return dict(self.get_graph())

    def estCyclique(self, s: Union[str,int], isindex=True) -> Tuple[bool,list[str]]:
        """parcours la matrice d'adjacence et renvoie si le graphe est cyclique ou non"""
        if isindex: 
            u = s
        else :
            u = self.liste.index(s)
        parcours = []
        file = []
        visites = [False] * self.n
        visites[u] = True 
                    
        parent = [-1] * self.n  # Pour mémoriser à partir de quel sommet on a découvert chaque commet du graphe
        parent[u] = u  # Au départ le parent de u est u lui même
        file.append(u)
        while file:
            courant = file.pop(0)
            visites[courant] = True
            parcours.append(self.liste[courant])
            for i in range(self.n):
                if self.M[courant][i] > 0 and visites[i] == False:
                    file.append(i)
                    visites[i] = True
                    parcours.append(self.liste[i])
                    parent[i] = courant # Parent de i est le noeud courant

                elif self.M[courant][i] > 0 and visites[i] == True and parent[courant] != i: # Si i est un noeud adjacent déjà visité et i n'est pas le parent de courant
                    return True,parcours # donc il y a un cycle, retourner True
        return False,parcours # pas de chemin entre u et u


class Graph:
    '''créer un graphe (vide ou à partir de noms de sommets)'''
    def __init__(self, *args: str):
        self.graph = {}
        for arg in args:
            self.add_sommet(arg)

    def  __dict__(self) -> dict:
        """renvoie le dictionnaire du graph"""
        return self.graph
    def __repr__(self):
        """affiche le graphe"""
        return f"Graph({self.graph})"
    def __len__(self) -> int :
        """retourne la taille du graph"""
        return len(self.graph)
    def __getitem__(self, nom: str) -> list:
        """retourne les sommets adjacents"""
        return self.sommet_adj(nom)
    def __contains__(self,x):
        """retourne si x est dans le graph"""
        return x in self.graph

    def len_arrete(self) -> int:
        """retourne le nombre d'arrete dans le graph"""
        return reduce(lambda acc, el: len(self.graph[el]) + acc, self.graph.keys(), 0) // 2
                    #accumulateur, elment fonction len + accumulatteur dans self.graph, valeur par defaut

        # return sum([len(self.graph[string]) for string in self.graph]) // 2
    
    def add_sommet(self, nom: str):
        """ajoute un sommet au graph"""
        if nom not in self.graph:
            self.graph[nom] = []

    def add_sommet_args(self, *args):
        """ajoute des sommets au graph"""
        for arg in args :
            self.add_sommet(arg)
        
    def add_arrete(self, nom1: str, nom2: str) -> bool:
        """ajoute une arrete au graph et retourne si ils on bien été ajouté"""
        if nom1 in self.graph and nom2 in self.graph :
            if nom1 not in self.graph[nom2] and nom2 not in self.graph[nom1] :
                self.graph[nom1].append(nom2)
                self.graph[nom2].append(nom1)
                return True
        return False

    def arrete_existe(self, nom1: str, nom2: str) -> bool:
        """Renvoie si une arrete existe ou non dans le graph"""
        if nom1 in self.graph and nom2 in self.graph :
            if nom1 in self.graph[nom2] and nom2 in self.graph[nom1] :
                return True
        return False

    def add_arrete_args(self, nom1: str, *args: str):
        """ajoute des arretes au graph, entre un sommet et tout les autres"""
        for arg in args :
            if arg != nom1 :
                self.add_arrete(nom1,arg)
    
    def relier_arretes(self, *args: str):
        """relie des sommets entres eux"""
        l = list(args)
        for i in range(1, len(l)):
            self.add_arrete(l[i-1],l[i])
    
    def del_arrete(self,nom1: str,nom2: str):
        """supprime une arrete du graphe"""
        self.graph.get(nom1, []).remove(nom2)
        self.graph.get(nom2, []).remove(nom1)

    def del_sommet(self,nom: str):
        """supprime un sommet du graphe"""
        for sommet in self.graph[nom]:
            self.del_arrete(nom, sommet)
        del self.graph[nom]

    def est_vide(self) -> bool:
        """retourne vraie ou faux si le graph est vide ou non"""
        return self.graph == {}

    def sommet_adj(self,nom: str) -> list :
        """retourne les sommets adjacent a un sommet donnée"""
        return self.graph.get(nom, [])
    
    def degre(self,nom: str) -> int :
        """retourne le degré d'un sommet"""
        return len(self.graph.get(nom, []))

    def plusgrandegre(self) -> dict:
        """retourne l'element de degré le plus haut"""
        c = list(self.graph.items())
        for element in c :
            if len(element[1]) == max([len(self.graph[elm]) for elm in self.graph]):
                return {element[0]:element[1]}
    
    def voisin(self,nom: str) -> list :
        """retourne les voisin d'un Noeud"""
        return self.sommet_adj(nom)
    
    def from_dico(self,d: dict):
        """import des sommets et des arretes a partire d'un dictionnaire"""
        [self.add_sommet(sommets) for sommets in d]
        for sommets in d :
            self.add_arrete_args(sommets, *d[sommets])

    def from_other_graph(self,g: Graph):
        """import des sommets et des arretes a partire d'un autre graph"""
        self.from_dico(g.__dict__())

    def changernom(self,sommet: str, nom: str):
        """change le nom d'un sommet"""
        self.graph[nom] = self.graph.pop(sommet)

    def get_matrice(self) -> Matrice:
        """Retourne la matrice d'adjacence du graphe"""
        liste = list(self.graph.keys())
        n = len(liste)
        M = [[0]*n for i in range(n)]
        for i in range(n):
            for j in range(n):
                if liste[j] in self.graph[liste[i]]:
                    M[i][j]=1
        return Matrice(liste,M)

    def fusion(self, graphex: Graph) :
        """fisionne deux graphes"""
        F = Graph()
        F.from_dico(self.__dict__() | graphex.__dict__())
        return F

    def parcours_largeur(self,sommet:str) -> list :
        """parcours en largeur du graphe"""
        sommet_visite = []
        f = File()
        f.enfiler(sommet)
        while not f.vide() :
            tmp = f.defiler()
            if tmp not in sommet_visite :
                sommet_visite.append(tmp)
            for elem in self.sommet_adj(tmp) :
                if elem not in sommet_visite and elem not in f :
                    f.enfiler(elem)
        return sommet_visite
    
    def in_class_parcours_largeur_rec(self,f : File,sommets_visites: list):
        """parcours en largeur recursif du graphe fonction interne"""
        if f.vide():
            return sommets_visites
        tmp = f.defiler()
        for u in self.sommet_adj(tmp):
            if u not in sommets_visites:
                sommets_visites.append(u)
                f.enfiler(u)
        return self.in_class_parcours_largeur_rec(f,sommets_visites)
    
    def parcours_largeur_rec(self,sommet):
        """parcours en largeur recursif du graphe"""
        f = File()
        f.enfiler(sommet)
        sommet_v = []
        sommet_v.append(sommet)
        c = self.in_class_parcours_largeur_rec(f,sommet_v)
        return c 
    
    def parcours_largeur_dict(self,sommet: str) -> dict:
        """parcours en largeur du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs)"""
        parents = dict()
        sommet_visite = []
        f = File()
        f.enfiler(sommet)
        parents[sommet] = None
        while not f.vide() :
            tmp = f.defiler()
            if tmp not in sommet_visite :
                sommet_visite.append(tmp)
            for elem in self.sommet_adj(tmp) :
                if elem not in sommet_visite and elem not in f :
                    f.enfiler(elem)
                    parents[elem] = tmp
        return parents

    def parcours_largeur_dict_rec_in_class(self,f: File,sommets_visites: list,parents: dict):
        """parcours en largeur recursif du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs), methode interne a la class """
        if f.vide():
            return None
        tmp=f.defiler()
        for u in self.voisin(tmp):
            if u not in sommets_visites:
                sommets_visites.append(u)
                f.enfiler(u)
                parents[u] = tmp
        self.parcours_largeur_dict_rec_in_class(f,sommets_visites,parents)
        return parents

    def parcours_largeur_dict_rec(self, depart: str) -> dict:
        """parcours en largeur recursif du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs)"""
        parentsd = dict()
        parentsd[depart] = None
        f=File()
        sommets_visites=[]
        f.enfiler(depart)
        sommets_visites.append(depart)
        parents = dict(self.parcours_largeur_dict_rec_in_class(f,sommets_visites,parentsd))
        return parents
    
    def solution(self, end: str, parents: dict) -> list[str]:
        """affiche un chemin entre deux sommets grace aux dictionnaires sommets visités/parents"""
        chemin = []
        courant = end
        while courant != None:
            chemin = [courant] + chemin
            courant = parents[courant]
        return chemin

    def parcours_profondeur_alea(self, sommet: str) -> list[str]:
        """parcours en profondeur du graphe depuis des Noeuds aléatoires"""
        sommets_visites = []
        sommets_fermes = []
        p = Pile()
        sommets_visites.append(sommet)
        p.empiler(sommet)
        while p.vide() == False:
            tmp = p.sommet()
            voisins = [y for y in self.voisin(tmp) if y not in sommets_visites]
            if len(voisins) != 0:
                v = choice(voisins)
                sommets_visites.append(v)
                p.empiler(v)
            else:
                sommets_fermes.append(tmp)
                p.depiler()
        return sommets_fermes

    def parcours_profondeur_bis(self,sommet) -> list[str]:
        """parcours en profondeur du graphe depuis un Noeud fixe"""
        p=Pile()
        sommets_visites=[]
        p.empiler(sommet)
        while p.vide()==False:
            tmp=p.depiler()
            if tmp not in sommets_visites:
                sommets_visites.append(tmp)
            voisins=[y for y in self.voisin(tmp) if y not in sommets_visites]
            for vois in voisins:
                p.empiler(vois)
        return sommets_visites
    
    def parcours_profondeur_rec(self, sommet:str, sommets_visites=[]) -> list[str]:
        """parcours en profondeur recursif du graphe depuis un noeud fixe"""
        if sommet not in sommets_visites:
            sommets_visites.append(sommet)
        voisins = [y for y in self.voisin(sommet) if y not in sommets_visites]
        for vois in voisins:
            sommets_visites + self.parcours_profondeur_rec(vois, sommets_visites)
        return sommets_visites

    def parcours_profondeur_dict_rec_in_class(self,depart: str, sommets_visites: list[str], parents=dict()):
        """parcours en profondeur recursif du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs), methode interne a la class """
        if depart not in sommets_visites:
            sommets_visites.append(depart)
        voisins = [y for y in self.voisin(depart) if y not in sommets_visites]
        for vois in voisins:
            parents[vois] = depart
            parents, sommets_visites + self.parcours_profondeur_dict_rec_in_class(depart, sommets_visites, parents)
        return parents,sommets_visites

    def parcours_profondeur_dict_rec(self,sommet: str) -> dict:
        """parcours en profondeur recursif du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs)"""
        sommets_visites = []
        parents = dict()
        parents[sommet] = None
        def dfs2(self, depart):
            if depart not in sommets_visites:
                sommets_visites.append(depart)
            voisins = [y for y in self.voisin(depart) if y not in sommets_visites]
            for vois in voisins:
                parents[vois] = depart
                dfs2(self,vois)
        dfs2(self,sommet)
        return parents

    def parcours_profondeur_dict_bis(self,depart: str):
        """parcours en profondeur du graphe, retourne un dictionnaire qui contient les sommets visités(clés) et leurs parents(valeurs)"""
        sommets_visites = []
        parents = dict()
        parents[depart] = None
        p=Pile()
        p.empiler(depart)
        while p.vide()==False:
            depart = p.depiler()
            if depart not in sommets_visites:
                sommets_visites.append(depart)
            voisins=[y for y in self.voisin(depart) if y not in sommets_visites]
            for vois in voisins:
                p.empiler(vois)
                parents[vois] = depart
        return parents
    def EstCyclique(self,sommet: str) -> Tuple[bool,list[str]]:
        """Renvoie vraie si le graph contient au moins un cycle"""
        sommets_visites=[]
        f=File()
        sommets_visites.append(sommet)
        f.enfiler((sommet,-1))
        while f.vide()==False:
            (tmp,parent)=f.defiler()
            voisins=self.voisin(tmp)
            for vois in voisins:
                if vois not in sommets_visites:
                    sommets_visites.append(vois)
                    f.enfiler((vois,tmp))
                elif vois!=parent:
                    return True,sommets_visites
        return False,sommets_visites
    
    def MatriceEstCyclique(self,sommet) -> Tuple[bool,list[str]]:
        """Renvoie vraie si le graph contient au moins un cycle (utilise la matrice d'adjacence)"""
        M = self.get_matrice()
        return M.estCyclique(sommet,False)





if __name__ == '__main__': #quelques testes de la class Graph, Matrice ainsi que les parcours de graph

    print('Graph -----------------------------------------------------------------------------------')
    G = Graph('a','b','c','d','e','f','g','h')
    G.add_arrete('a','b')
    G.add_arrete('a','c')
    G.add_arrete('b','d')
    G.add_arrete('b','e')
    G.add_arrete('c','d')
    G.add_arrete('d','e')
    G.add_arrete('e','f')
    G.add_arrete('e','g')
    G.add_arrete('f','g')
    G.add_arrete('g','h')
    print('arretes de f', G['f'])
    print("nb d'arrete dans G :", G.len_arrete())
    print("element de plus grand degré :", G.plusgrandegre())
    print(G.get_matrice())

    print('Matrice -----------------------------------------------------------------------------------')
    A1=[[0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0]]
    liste=['a','b','c','d','e','f','g','h']
    MA1 = Matrice(liste,A1)
    print(MA1.get_graph())
    print(MA1.get_list())
    print(MA1.estCyclique('e',False))

    matriceAdj = [[0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 1, 0],
                [0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0]]
    mat = Matrice([1,2,3,4,5],matriceAdj)
    print(mat.estCyclique(0))
    if mat.estCyclique(0)[0] == True:
        print("Le graphe contient un cycle")
    else:
        print("Le graphe est acyclique")

    print('Parcours Graph -----------------------------------------------------------------------------------')
    print('parcours_largeur',G.parcours_largeur('g')) 
    print('parcours_largeur_rec',G.parcours_largeur_rec('g')) 
    print('parcours_largeur_dict',G.parcours_largeur_dict('b'))
    print('solution_parcours_largeur',G.solution('h',G.parcours_largeur_dict('b'))) 
    print('parcours_largeur_dict_rec',G.parcours_largeur_dict_rec('b'))
    print('solution_parcours_largeur',G.solution('h',G.parcours_largeur_dict_rec('b')))  
    print('parcours_profondeur_alea',G.parcours_profondeur_alea('g')) 
    print('parcours_profondeur_bis',G.parcours_profondeur_bis('g')) 
    print('parcours_profondeur_rec',G.parcours_profondeur_rec('g'))  
    print('parcours_profondeur_dict_rec',G.parcours_profondeur_dict_rec('g')) 
    print('solution_parcours_profondeur_rec',G.solution('h',G.parcours_profondeur_dict_rec('b')))  
    print('parcours_profondeur_dict_bis',G.parcours_profondeur_dict_bis('g'))
    print('solution_parcours_profondeur',G.solution('h',G.parcours_profondeur_dict_bis('b'))) 
    print('EstCyclique',G.EstCyclique('b')) 
    print('MatriceEstCyclique',G.MatriceEstCyclique('b')) 


    
    


