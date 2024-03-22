# **NSI projet 4 : Générateur et solveur de labyrinthe**

## **UTILISATION DU PROJET**

Pour le bon fonctionnement du programme les *bibliothèques tkinter,matplotlib, typing, PIL, customtkinter, math, random, networkx, time, numpy* a jours, **un fichier *libraries.bat* est disponible pour les installer et les mettre à jours directement**.

Pour exécuter le programme il faut ouvrir le dossier .***\Code Source*** contenant tous les fichiers **dans Visual studio code**, et exécuter le code depuis la page ***Générateur de Labyrinthe.py***

La page ci-dessous devrais apparaitre après l’exécution du fichier ***Générateur de Labyrinthe.py***

![1](images/1.png)

Vous pouvez aussi consulter et tester les fonctions propres à chaque classe du programme en ouvrant et en exécutant le fichier* approprié

Le programme possède plusieurs fonctionnalités, elles permettent entre autres de générer et de résoudre de plusieurs manière un labyrinthe de taille définie par l’utilisateur.

### **Fonctionnalité 1** -> *Générer un labyrinthe*

Ouvre une page de génération, ou on choisit la hauteur et la longueur du labyrinthe, puis on génère un labyrinthe et l’affiche.

Depuis la page affichée on peut, *retourner au menu principal*, *afficher le graph*, *enregistrer le labyrinthe*, de plus *Solution et parcours* affiche un menu flottant détaillé si dessous :

**Les parcours** -> Parcours le graphe **sans le résoudre**, permet de visualiser chaque type de parcours.

**Les cycles** -> Parcours le graph a la recherche de cycle, affiche un message s’il y’en a un.

**Les Solutions** -> Résous le labyrinthe de différentes manières

**L’algorithmes de Dijkstra** -> résous le labyrinthe avec une pondération aléatoire ou non 

**Graph** -> Afficher le graph pondéré ou redonner des poids aléatoires a toutes les arrêtes 

**Labyrinthe** -> Afficher la pondération, permet de l’afficher si on ne le pas fait depuis les paramètres, le paramètre ne sera pas sauvegardé dans le fichier config (notes : pour la désactiver il faut aller dans les paramètre et valider (vérifier que la case ne soit pas cochée)).





### **Fonctionnalité 2** -> *Importer un labyrinthe* 

Importer un labyrinthe depuis un fichier texte, provoque une erreur lorsque les fichiers ne sont pas dans le bon format.





### **Fonctionnalité 3** -> *Paramètre* 

Paramètres graphiques du graphe, de l’application et du labyrinthe, lorsque les paramètres sont validés cela les enregistre dans un fichier de configuration.


***Notes :***

***Entrée :***

L’entrée du labyrinthe est définie par l’icône ci-dessous (ou un point vert si le labyrinthe est trop grand ou si les images sont inaccessibles)

![](images/2.png)

***Sortie :***

La sortie du labyrinthe est définie par l’icône ci-dessous (ou un point rouge si le labyrinthe est trop grand ou si les images sont inaccessibles)

![](images/3.png)

***Performances :***

Générer un labyrinthe de plus de 70x70 peut causer des **problèmes de performance**, si vous générerez un labyrinthe ou un des coté est de plus de 70 cases le labyrinthe ne sera pas afficher entièrement il faudra ce déplacer avec l’outils de navigation en bas a gauche de la fenêtre.

Pour les parcours récursifs il est possibles que s’il y’a trop de case cela affiche une pop-up d’erreur car il y’a trop d’appel récursif, cela est réglé dans l’exécutable car lors du pack de celui-ci la limite a été repoussée.

