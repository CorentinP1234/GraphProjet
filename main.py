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
NUMBER = 0
DURATION = 1
PRED = 2


class constraints_table:
    def __init__(self, S, A) -> None:
        self.A = A
        self.S = S


class task:
    def __init__(self, num, duration, predecessors) -> None:
        self.num = num
        self.duration = duration
        self.predecessors = predecessors

    def __str__(self) -> str:
        return f"task({self.num}, {self.duration}, {self.predecessors})"

    def __repr__(self) -> str:
        return f"task({self.num}, {self.duration}, {self.predecessors})"


# 1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire
def read(file):
    tasks = []
    # Open file
    with open(file, 'r') as f:
        # Loop each line
        for line in f.read().splitlines():
            words = line.split()
            task_num = int(words[0])
            duration = int(words[1])
            predecessors = list(map(int, words[2:]))
            new_task = task(task_num, duration, predecessors)
            tasks.append(new_task)
    return tasks

# 2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet
# affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier.
# Ce graphe doit incorporer les deux sommets fictifs a et w (notés 0 et N+1 où N est le nombre
# de tâches).


def getAdjacentMatrix(tasks) -> list:
    # N is the number of tasks
    N = len(tasks)
    m = [[0] * (N+1) for _ in range(N+1)]
    for task in tasks:
        for predecessor in task.predecessors:
            m[task.num][predecessor] = 1
    return m


def choose_constraints():
    ...


def readConstraints():
    ...


def getConstraintsMatrix():
    ...


def print_matrix(m):
    # Print first line
    for i in range(len(m[0])):
        if i != len(m[0])-1:
            print(str(i) + "| ", end="")
        else:
            print(i)
    for i in range(len(m)+1):
        for j in range(len(m[0])):
            print(f"{m[i][j]} |")


def checkOrdonnancement():
    ...


def getNodeRanks():
    ...


def getSchedules():
    ...


def askUserForConstraints():
    ...


def main():
    # Tant que l’utilisateur décide de tester un tableau de
    # contraintes faire
    constraints_remaing = True
    while (constraints_remaing):
        # Choise le tableau de contraintes a traiter
        constraints_number = choose_constraints()
        # Lire le tableau de contraintes sur fichier et le stocker en mémoire
        constraints_dict = readConstraints(constraints_number)

        # Créer la matrix correspondant au graphe repésentant ce tableau de
        # contraintes et l'afficher
        constraints_matrix = getAdjacentMatrix()
        print_matrix()
        # Verifier que l es proprietes necessaires pur que ce graphe
        # soit un graphe d'ordonnacement sont verifiees
        if (checkOrdonnancement()):
            # Si oui alors
            # Calculer les rans des sommets et les afficher
            node_ranks = getNodeRanks()
            # Calculer les calendriers au plus tot
            shedules = getSchedules()
            # et au plus tard et les afficher
        else:
            # Sinon
            # Proposer à l'utilisateur de changer de tableau de contraintes
            askUserForConstraints()


if __name__ == "__main__":
    tasks = read('example_1.txt')
    matrix = getAdjacentMatrix(tasks)
    print_matrix(matrix)
