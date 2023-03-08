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

# Assumptions :
# - durations doesn't exceed 99 unit of time (printing issues)

from C7_Graph import *

""" 1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire"""


def read_constraints_table(file):
    """This function return a graph object containing the table information or None if an error occurred"""
    name = file[:-4]
    g = Graph(name)
    
    # Open the file
    try:
        with open(file, 'r') as f:
            
            print(f"{COLORS.OKBLUE}* Creation du graphe d'ordonnancement {file}:{COLORS.ENDC}\n")
            
            # Read each line of the input file
            for num_line, line in enumerate(f.read().splitlines()):
                
                # Extract task number, duration, and predecessors from the line
                task_id, duration, *predecessors = map(int, line.split())
                
                # Check if the input is valid
                if not (task_id > 0 and (0 < duration < 100) and all(x > 0 for x in predecessors)):
                    # Print Error message and return None
                    print(f"{COLORS.FAIL}Error: this table is not valid:")
                    print(f"At line {num_line + 1}: {line}{COLORS.ENDC}")
                    return None
                
                # Add the node and its duration to the graph
                g.add_node(task_id, duration)
                # If the task has predecessors, add edges pred -> task_num
                g.add_edges(predecessors, task_id)
                
                # If not, add an edge 'alpha' -> task_num
        g.add_omega_node()
        g.add_omega_edges()
        print(f"{COLORS.OKGREEN}Création du graphe {name} réussie{COLORS.ENDC}\n")
        g.print()
        return g
    
    except FileNotFoundError:
        print(f"{COLORS.FAIL}Error: this file doesn't exists {file}{COLORS.ENDC}")
        return None


""" 2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet
 affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier.
 Ce graphe doit incorporer les deux sommets fictifs à et w (notés 0 et N+1 où N est le nombre
 de tâches)."""


def print_adjacency_matrix(graph):
    print(f" {COLORS.UNDERLINE}Matrice des valeurs de {graph.name}{COLORS.ENDC}", end="\n  ")
    # Print first line
    print(f"  {COLORS.UNDERLINE}", end="")
    for node in graph.node_ids:
        print("%2.d " % node, end="")
    # print("", end="\n\t")
    print(f"{COLORS.ENDC}", end="\n ")
    # Print each line
    for from_node in graph.node_ids:
        print("%2.d|" % from_node, end="")
        first_iteration = True
        for to_node in graph.node_ids:
            dur = graph.adjacency_matrix[from_node][to_node]
            shift = "" if first_iteration else " "
            if dur == ".":
                print(shift + " %s" % dur, end="")
            else:
                print(" %2.d" % int(dur), end="")
            first_iteration = False
        print("", end="\n ")
    print()


def choose_constraints_table():
    choix = input("Choix du tableau de contraintes a traiter :")
    file = f"table {choix}.txt"
    return file


def is_acyclic(graph):
    # Methode de suppression des points d'entrée
    print(f"{COLORS.OKBLUE}* Détection de circuit{COLORS.ENDC}")
    print(f"{COLORS.OKBLUE}* Méthode d'élimination des points d'entrée{COLORS.ENDC}\n")
    
    suppressed_nodes = set()
    nodes_remaining = graph.node_ids.copy()
    
    while len(nodes_remaining) > 0:
        print(f"suppressed : {suppressed_nodes}")
        starting_nodes = graph.get_nodes_with_no_predecessors(suppressed_nodes)
        print(f"Point d'entrée : {starting_nodes}")
        print("Suppression des points d'entrée")
        nodes_remaining -= starting_nodes
        # If there are no starting nodes, it means we cannot remove nodes anymore, the graph is cyclic
        if not starting_nodes:
            return False
        if nodes_remaining:
            print(f"Sommets restant : {nodes_remaining}")
        else:
            print(f"Sommets restant : Aucun\n")
        suppressed_nodes = suppressed_nodes.union(starting_nodes)
    return True


def has_negative_edges(graph):
    for node, dur in graph.duration_of.items():
        if dur < 0:
            print(f"Task {node} has a negative duration {dur}")
            return True
    return False


def check_scheduling_graph(graph):
    # Print entry points
    nodes = sorted(graph.node_ids)
    print(f"Il y a un seul point d'entré, {nodes[0]}")
    print(f"Il y a un seul point de sortie, {nodes[-1]}\n")
    
    # Check if graph is acyclic
    if is_acyclic(graph):
        
        print("-> Il n'y a pas de circuit")
        print("Les valeurs pour tous les arcs incidents \
        vers l'extérieur à un sommet sont identiques")
        successors = graph.get_successors(0)
        num_successors = len(successors)
        
        if num_successors == 1:
            print(fr"L'arc 0->{successors[0]} est nul")
        else:
            print("Les arcs", end="")
            for i, succ in enumerate(successors):
                if i != num_successors - 1:
                    print(f" 0->{succ}", end="")
                else:
                    print(f" et 0->{succ}")
        if not has_negative_edges(graph):
            print("Il n'y a pas d'arcs négatifs")
            print("-> C'est un graphe d'ordonnancement")
            return True
        else:
            print("Il y a au moins un arc négatif")
            print("-> C'est n'est pas un graphe d'ordonnancement")
            return False
    else:
        print("-> Il y a un circuit ")
        print("-> C'est n'est pas un graphe d'ordonnancement")
        return False


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
        graph.adjacency_matrix = graph.get_adjacency_matrix()
        print_adjacency_matrix(graph)
        # Verifier que les propriétés nécessaires pour que ce graphe
        # soit un graphe d'ordonnancement sont vérifiées
        print(f"res = {check_scheduling_graph(graph)}")
        exit()
        if True:
            # Si oui alors
            # Calculer les rangs des sommets et les affiche
            node_ranks = get_node_ranks()
            # Calculer les calendriers au plus tot
            schedules = get_schedules()
            # et au plus tard et les affiche
        else:
            # Sinon
            # Proposer à l'utilisateur de changer de tableau de contraintes
            ask_user_for_table()


if __name__ == "__main__":
    main()
    exit()
