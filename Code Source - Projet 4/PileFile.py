class Pile:
    ''' classe Pile
    création d'une instance Pile avec une liste
    '''
    def __init__(self):
        "Initialisation d'une pile vide"
        self.L=[]
    def vide(self):
        "teste si la pile est vide"
        return self.L==[]
    def depiler(self):
        "dépile"
        assert not self.vide(),"Pile vide"
        return self.L.pop()
    def empiler(self,x):
        "empile"
        self.L.append(x)
    def taille(self):
        return len(self.L)
    def sommet(self):
        return self.L[-1]
    def __contains__(self,x):
        return x in self.L
    def __repr__(self):
        print('Pile :', self.L)
        return 'Pile :' + ''.join(map(str, self.L))

class File:
    ''' classe File
    création d'une instance File avec une liste
    '''
    def __init__(self):
        self.L = []
    def vide(self):
        return self.L == []
    def defiler(self):
        assert not self.vide(), "file vide"
        return self.L.pop(0)
    def enfiler(self,x):
        self.L.append(x)
    def __len__(self):
        return len(self.L)
    def sommet(self):
        return self.L[0]
    def __contains__(self,x):
        return x in self.L