"""
1. Lecture d un tableau de contraintes contenu dans un fichier .txt, mise en
mémoire et affichage de ce tableau sur l écran ;
2. Construction d un graphe correspondant à ce tableau de contraintes ;
3. Vérification du fait que ce graphe possède toutes les propriétés nécessaires pour
qu il soit un graphe d ordonnancement :
o Un seul point d entrée
o Un seul point de sortie
o Pas de circuit
o Valeurs identiques pour tous les arcs incidents vers l extérieur à un
sommet,
o Arcs incidents vers l extérieur au point d entrée ont une valeur nulle,
o Pas d arcs à valeur négative.
4. Si toutes ces propriétés sont vérifiées, calculer le calendrier au plus tôt, la durée
totale de projet, le calendrier au plus tard et les marges.
Pour le calcul du calendrier au plus tard, utilisez la convention que la date au
plus tard de fin de projet soit égale à sa date au plus tôt.
Comme vous savez, pour le calcul des calendriers il faut d abord effectuer le
tri topologique du graphe : ordonner les sommets dans l ordre des rangs
croissants. Il faut donc affecter un rang à chaque sommet, en utilisant un
algorithme de votre choix parmi ceux que vous avez vu en cours.
"""
import copy
#1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire
def read(file):
  tasks = {}
  # Open file
  with open(file, 'r') as f:
    # Loop for
    for line in f.read().splitlines():
      words = line.split()
      tasks_number = int(words[0])
      predecessors = []

      # processing predecessors
      for word in words[1:]:
        # Convert to integers
        predecessors.append(int(word)) 

      # Add a task and its predecessors to a map : 
      # task_number => [p1, p2, p3, ...]
      tasks[tasks_number] = predecessors
    return tasks

#2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet
# affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier.
# Ce graphe doit incorporer les deux sommets fictifs a et w (notés 0 et N+1 où N est le nombre
# de tâches). 
def toMatrix(tasks):
  # N is the number of tasks
  N = len(tasks.keys())
  m = [([0] * N+1) for _ in range(N+1)]
  for task in tasks.keys():
    for predecessor in  tasks[task]:
      m[predecessor] = 
  print(m)

def choose_constraints():
  ...
def readConstraints():
  ...
def getConstraintsMatrix():
  ...


def main():
  # Tant que l’utilisateur décide de tester un tableau de
  # contraintes faire
  constraints_remaing = True
  while(constraints_remaing):
    # Choise le tableau de contraintes a traiter
    constraints_number = choose_constraints()
    #Lire le tableau de contraintes sur fichier et le stocker en mémoire
    constraints_dict = readConstraints(constraints_number)

    # Créer la matrix correspondant au graphe repésentant ce tableau de
    # contraintes et l'afficher
    constraints_matrix = getConstraintsMatrix()
    # Verifier que l es proprietes necessaires pur que ce graphe
    # soit un graphe d'ordonnacement sont verifiees

        #Si oui alors
        # Calculer les rans des sommets et les afficher
        # Calculer les calendriers au plus tot 
        # et au plus tard et les afficher

        #Sinon
        # Proposer à l'utilisateur de changer de tableau de contraintes
    #fin Tant que
    ...
    


tasks = read('example_1.txt')
matrix = toMatrix(tasks)