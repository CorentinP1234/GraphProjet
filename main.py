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


class Edge:
    def __init__(self, start_node, end_node, duration):
        self.start = start_node
        self.end = end_node
        self.dur = duration

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end} = {self.dur}"

    @staticmethod
    def print(edge_list):
        for edge in edge_list:
            print(edge)


class Graph:
    # self.adj_list[from_node][to_node] = self.durationOf[from_node]
    def __init__(self):
        self.durationOf: dict = {0: 0}
        self.all_ids: set = set()
        self.adj_list: dict = {}

    def add_edge(self, from_node, to_node, specific_duration=None):
        if from_node not in self.adj_list:
            self.adj_list[from_node] = []
        if specific_duration:
            self.durationOf[from_node] = specific_duration
            self.adj_list[from_node].append(to_node)
        else:
            self.adj_list[from_node].append(to_node)

    def get_successors(self, node):
        if node not in self.adj_list:
            return []
        return list(self.adj_list[node])

    def get_duration(self, from_node, to_node):
        if from_node in self.adj_list:
            if to_node in self.adj_list[from_node]:
                return self.durationOf[from_node]
        return None
    
    def add_omega_edges(self):
        nodes_with_ex_edge = self.adj_list.keys()
        N = len(self.all_ids)
        for node_id in self.all_ids:
            if node_id not in nodes_with_ex_edge:
                self.add_edge(node_id, N+1)
        # Add N+1 node
        self.all_ids.add(N + 1)

    def print(self):
        for from_node, to_nodes in sorted(self.adj_list.items()):
            for to_node in to_nodes:
                print(f"{from_node} -> {to_node} = {self.durationOf[from_node]}")

# 1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire
# read (file): given a file, return a tuple containing a list of nodes ids (numbers) and a list of edges (edge objects)

def read_constraints_table(file):
    g: Graph = Graph()

    with open(file, 'r') as f:

        print(f"* Creation du graphe d'ordonnancement {file[:-4]}:")

        # 1. Read the input file and create Task objects from each line

        for line in f.read().splitlines():
            # Extract task number, duration, and predecessors from the line
            task_num, duration, *predecessors = map(int, line.split())

            g.all_ids.add(task_num)
            g.durationOf[task_num] = duration

            # Check if the input is valid
            if not (task_num > 0 and duration > 0 and all(x > 0 for x in predecessors)):
                raise "Error: this table is not valid."

            if predecessors:
                for pred in predecessors:
                    g.add_edge(pred, task_num)
            else:
                g.add_edge(0, task_num, 0)

    g.add_omega_edges()  # Add noe N+1 and omega edges
    g.print()
    return g


# 2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet
# affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier.
# Ce graphe doit incorporer les deux sommets fictifs a et w (notés 0 et N+1 où N est le nombre
# de tâches).

def getAdjacentMatrix(graph: Graph) -> list:
    N = len(graph.all_ids)
    m = [['*'] * (N + 2) for _ in range(N + 1)]
    for from_node in graph.all_ids:
        for to_node in graph.adj_list.get(from_node, []):
            m[from_node][to_node] = graph.durationOf[from_node]
    return m


def choose_constraints_table():
    choix = input("Choix du tableau de contraintes a traiter :")
    file = f"table {choix}.txt"
    return file


def getConstraintsMatrix():
    ...


def print_matrix(m):
    size_cell = len(str(len(m))) + 1
    print((size_cell - 1) * " " + " | ", end="")
    # Print first line
    for i in range(len(m[0])):
        if i != len(m[0]) - 1:
            print(str(i) + (size_cell - len(str(i))) * " " + " ", end="")
        else:
            print(i)
    print((((len(m) + 2) * 4) - 1) * "-")
    for i in range(len(m) + 1):
        for j in range(len(m[0]) + 1):
            if j == 0:
                print(str(i) + (size_cell - len(str(i)))
                      * " " + "|", end="")
            else:
                print(f" {m[i - 1][j - 1]}  ", end="")
        print()


def check_scheduling_graph():
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
    constraints_remaining = True
    while constraints_remaining:
        # Choix le tableau de contraintes à traiter
        # file_name = choose_constraints_table()
        file_name = "table 0.txt"
        # Lire le tableau de contraintes sur fichier et le stocker en mémoire
        graph = read_constraints_table(file_name)

        # Créer la matrix correspondant au graphe représentant ce tableau de
        # contraintes et l'afficher
        constraints_matrix = getAdjacentMatrix(graph)
        exit()
        print_matrix()
        # Verifier que les propriétés nécessaires pour que ce graphe
        # soit un graphe d'ordonnancement sont vérifiées
        if check_scheduling_graph():
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
    main()
    exit()
    # node_ids, tasks, starting_nodes_ids = read('example_2.txt')
    edges = get_edges(node_ids, tasks, starting_nodes_ids)
    matrix = getAdjacentMatrix(node_ids, edges)
    print_matrix(matrix)
