"""
1. Lecture d'un tableau de contraintes contenu dans un fichier .txt, mise en
    mémoire et affichage de ce tableau sur l'écran ;
2. Construction d'un graphe correspondant à ce tableau de contraintes ;
3. Vérification du fait que ce graphe possède toutes les propriétés nécessaires pour
    qu'il soit un graphe d'ordonnancement :
        o Un seul point d'entrée
        o Un seul point de sortie
        o Pas de circuit
        o Valeurs identiques pour tous les arcs incidents vers l'extérieur à un
        sommet,
        o Arcs incidents vers l'extérieur au point d'entrée ont une valeur nulle,
        o Pas d'arcs à valeur négative.
4. Si toutes ces propriétés sont vérifiées, calculer le calendrier au plus tôt, la durée
    totale de projet, le calendrier au plus tard et les marges.
    Pour le calcul du calendrier au plus tard, utilisez la convention que la date au
    plus tard de fin de projet soit égale à sa date au plus tôt.
    Comme vous savez, pour le calcul des calendriers, il faut d'abord effectuer le
    tri topologique du graphe : ordonner les sommets dans l'ordre des rangs
    croissants. Il faut donc affecter un rang à chaque sommet, en utilisant un
    algorithme de votre choix parmi ceux que vous avez vus en cours.
"""


class Graph:
    # self.adj_list[from_node][to_node] = self.durationOf[from_node]
    def __init__(self, name):
        self.name = name
        self.predOf = {}
        self.succOf = {0: set()}
        self.durationOf = {0: 0}
        self.node_ids = {0}
        self.num_of_edges = 0
        self.omega_id = None
        self.adjacency_matrix = None
    
    def add_node(self, node_id):
        if node_id in self.node_ids:
            print(f"Warning : Tache {node_id} a deja été ajouté")
        self.node_ids.add(node_id)
    
    def num_node(self):
        return len(self.node_ids)
    
    def get_num_edges(self):
        return self.num_of_edges
    
    def add_duration(self, task_num, duration):
        if task_num in self.durationOf:
            print(f"Warning : Tache {task_num} avait pour durée {duration[task_num]}\
             et va être écrasé par {duration}")
        self.durationOf[task_num] = duration
    
    def add_successor(self, node_id, succ):
        if node_id not in self.succOf:
            self.succOf[node_id] = set()
        self.succOf[node_id].add(succ)
    
    def add_predecessor(self, node_id, pred):
        if node_id not in self.predOf:
            self.predOf[node_id] = set()
        self.predOf[node_id].add(pred)
    
    def get_successors(self, node_id) -> tuple[int]:
        return self.succOf.get(node_id, set())
    
    def get_predecessors(self, node_id):
        return self.predOf.get(node_id, set())
    
    def add_omega_node(self):
        omega = len(self.node_ids)
        self.add_node(omega)
        self.omega_id = omega
    
    def add_edge(self, from_node, to_node):
        # Update set of predecessors
        self.add_predecessor(to_node, from_node)
        
        # Update set of successors
        self.add_successor(from_node, to_node)
        
        # Update the number of edges
        self.num_of_edges += 1
    
    def add_omega_edges(self):
        nodes_with_ex_edge = self.succOf.keys()
        for node_id in self.node_ids - {self.omega_id}:
            if node_id not in nodes_with_ex_edge:
                self.add_edge(node_id, self.omega_id)
    
    def get_nodes_with_no_predecessors(self, ignore=None):
        if ignore is None:
            ignore = set()
        return self.node_ids - (set(self.predOf.keys()).union(ignore))
        
    def print(self):
        print("Graphe d'ordonnancement de " + self.name)
        print(f"{len(self.node_ids)} sommets")
        print(f"{self.num_of_edges} arcs")
        for from_node, to_nodes in sorted(self.succOf.items()):
            for to_node in to_nodes:
                duration = self.durationOf[from_node]
                print(f"{from_node} -> {to_node} = {duration}")
        print()

    def get_adjacency_matrix(self) -> list:
        num_nodes = self.num_node()
        adjacency_matrix: list[list[str]] = [['*'] * num_nodes for _ in range(num_nodes)]
        for from_node in self.node_ids:
            for to_node in self.get_successors(from_node):
                adjacency_matrix[from_node][to_node] = self.durationOf[from_node]
        return adjacency_matrix
    
    def print_adjacency_matrix(self):
        print(" Matrice des valeurs")
        # Print first line
        print(" " * 3, end="")
        for node in self.node_ids:
            print("%2.d " % node, end="")
        print()
        # Print each line
        for from_node in self.node_ids:
            print("%2.d" % from_node, end="")
            for to_node in self.node_ids:
                dur = self.adjacency_matrix[from_node][to_node]
                if dur == "*":
                    print("  %s" % dur, end="")
                else:
                    print(" %2.d" % int(dur), end="")
            print()
        print()


# 1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire
# read (file): given a file, return a tuple containing a list of nodes ids (numbers) and a list of edges (edge objects)
def read_constraints_table(file):
    name = file[:-4]
    g: Graph = Graph(name)
    
    # Open the file
    try:
        with open(file, 'r') as f:
            
            print(f"* Creation du graphe d'ordonnancement {file}:\n")
            
            # 1. Read the input file and create Task objects from each line
            
            for line in f.read().splitlines():
                # Extract task number, duration, and predecessors from the line
                task_num, duration, *predecessors = map(int, line.split())
                
                # Check if the input is valid
                if not (task_num > 0 and (0 < duration < 100) and all(x > 0 for x in predecessors)):
                    raise "Error: this table is not valid."
                
                g.add_node(task_num)
                g.add_duration(task_num, duration)
                
                # If the task has predecessors, add edges pred -> task_num
                if predecessors:
                    for pred in predecessors:
                        g.add_edge(pred, task_num)
                # If not, add an edge 'alpha' -> task_num
                else:
                    g.add_edge(0, task_num)
        
        g.add_omega_node()
        g.add_omega_edges()
        g.print()
        
    except FileNotFoundError:
        raise f"Erreur: {file} n'existe pas"
    
    return g


# 2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet
# affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier.
# Ce graphe doit incorporer les deux sommets fictifs a et w (notés 0 et N+1 où N est le nombre
# de tâches).

def get_adjacency_matrix(graph: Graph) -> list:
    num_nodes = graph.num_node()
    adjacency_matrix = [['*'] * num_nodes for _ in range(num_nodes)]
    for from_node in graph.node_ids:
        for to_node in graph.get_successors(from_node):
            adjacency_matrix[from_node][to_node] = graph.durationOf[from_node]
    return adjacency_matrix


def choose_constraints_table():
    choix = input("Choix du tableau de contraintes a traiter :")
    file = f"table {choix}.txt"
    return file


def is_cyclic(graph):
    # Methode de suppression des points d'entrée
    print("* Détection de circuit")
    print("* Méthode d'élimination des points d'entrée")
    
    suppressed_nodes = set()
    nodes_remaining = graph.node_ids.copy()
    
    while len(nodes_remaining) > 0:
        print(f"supressed : {suppressed_nodes}")
        starting_nodes = graph.get_nodes_with_no_predecessors(suppressed_nodes)
        print(f"Point d'entrée : {starting_nodes}")
        print("Suppression des points d'entrée")
        nodes_remaining -= starting_nodes
        print(f"Sommets restant : {nodes_remaining}")
        suppressed_nodes.union(starting_nodes)
        exit()
    exit()


def check_scheduling_graph(graph):
    nodes = sorted(graph.node_ids)
    print(f"Il y a un sel point d'entré, {nodes[0]}")
    print(f"Il y a un seul point de sortie, {nodes[-1]}")
    if is_cyclic(graph):
        ...
    exit()


def get_node_ranks():
    ...


def get_schedules():
    ...


def ask_user_for_table():
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
        graph.adjacency_matrix = graph.get_adjacency_matrix
        graph.print_adjacency_matrix()
        # Verifier que les propriétés nécessaires pour que ce graphe
        # soit un graphe d'ordonnancement sont vérifiées
        if check_scheduling_graph(graph):
            # Si oui alors
            # Calculer les rangs des sommets et les affiche
            node_ranks = get_node_ranks()
            # Calculer les calendriers au plus tot
            shedules = get_schedules()
            # et au plus tard et les affiche
        else:
            # Sinon
            # Proposer à l'utilisateur de changer de tableau de contraintes
            ask_user_for_table()


if __name__ == "__main__":
    main()
    exit()
