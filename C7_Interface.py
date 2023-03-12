

# ====================   INPUT   ==================================

def ask_user_for_table(n, default=None):
    printTitle("* Choix de la table de tache :\n")
    if default:
        return default
    while True:
        try:
            choice = int(input(f"Entrez un nombre entre 1 et {n}: \n{COLORS.GREEN}>{COLORS.END} "))
            if choice < 1 or choice > n:
                print(f"Choix invalide. Veuillez entrer un nombre entre 1 et {n}.\n")
            else:
                nom_fichier = f"table {choice}.txt"
                print()
                return nom_fichier
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def ask_for_an_other_table():
    while True:
        try:
            answer = input("\nVoulez-vous traiter une autre table ? (O/N) : ").lower()
            if answer == "o" or answer == "oui":
                return True
            elif answer == "n" or answer == "non":
                return False
            else:
                print("Veuillez répondre par 'Oui' (O) ou 'Non' (N).")
        except KeyboardInterrupt:
            print("Interruption de programme.")
            return None


# ====================   AFFICHAGE   ==================================

SHIFT = " " * 3


def print_graph(graph):
    # Affiche le nombre de sommets et d'arcs
    printShift(f"{len(graph.node_ids)} sommets")
    printShift(f"{graph.number_of_edges} arcs")
    # Parcours tous les nœuds avec leurs prédecesseurs et affiche la durée de chaque arc
    for to_node, from_nodes in (graph.predecessors_of.items()):
        for from_node in from_nodes:
            duration = graph.duration_of[from_node]
            printShift(f"{from_node} -> {to_node} = {duration}")
    print()


def print_adjacency_matrix(graph):
    if graph:
        # Titre de la matrice
        printTitle(f"* Matrice des valeurs de {graph.name} :", end="\n\n  ")
        
        # Affichage de la première ligne
        printShift(f" {COLORS.UNDERLINE}", end="")
        for node in graph.node_ids:
            print("%2.d " % node, end="")
        print(f"{COLORS.END}", end="\n")
        
        # Affichage de chaque ligne
        for from_node in graph.node_ids:
            # Affichage de l'identifiant de la ligne
            printShift("%2.d|" % from_node, end="")
            
            # Initialisation de la première itération
            first_iteration = True
            last_iteration = False
            if from_node == len(graph.node_ids) - 1:
                last_iteration = True
            
            # Affichage de chaque colonne
            for to_node in graph.node_ids:
                # Récupération de la durée de l'arc entre les deux nœuds
                dur = graph.adjacency_matrix[from_node][to_node]
                
                # Affichage d'un espace avant la valeur sauf pour la première itération
                shift = " "
                if first_iteration:
                    shift = ""
                prefix = ""
                if last_iteration:
                    prefix = f"{COLORS.UNDERLINE}"
                
                # Si l'arc existe, affichage de sa durée, sinon affichage d'un point
                if dur != -1:
                    print(prefix + " %2.d" % dur, end="")
                else:
                    print(prefix + shift + " .", end="")
                
                # Fin de la première itération
                first_iteration = False
                
                if to_node == len(graph.node_ids) - 1:
                    print(f" {COLORS.END}|", end="")
            
            # Passage à la ligne suivante
            print()
        
        # Passage à la ligne suivante pour aérer l'affichage
        print()


def print_schedule_line(string, remaining_space):
    shift = 1
    if remaining_space % 2 == 0:
        shift = 0
    return (remaining_space // 2) * " " + string + ((remaining_space // 2) + shift) * " "


def print_schedules(calendrier_tot, calendrier_tard):
    # Titre de la section
    printTitle("\n* Calendriers :\n")
    
    if len(calendrier_tard) != len(calendrier_tot):
        raise "Error: in print_schedules: Verifiez que les calendriers au plus tard et au plus tot sont de meme " \
              "tailles"
    
    # Espacement avant chaque ligne
    shift = "  "
    
    # Titres des colonnes
    title1 = "Taches"
    title2 = "Dates au plus tot"
    title3 = "Dates au plus tard"
    
    # Tailles des colonnes
    size1 = len(title1)
    size2 = len(title2)
    size3 = len(title3) + 1
    
    # Affichage des titres
    print(shift, end="")
    print(f" {COLORS.UNDERLINE}{COLORS.BOLD} {title1}   {title2}   {title3} {COLORS.END}")
    
    # Variable pour indiquer si on est sur la dernière ligne
    is_last_line = False
    
    # Parcours des tâches dans l'ordre de la liste des identifiants
    for task in range(len(calendrier_tard)):
        if task == len(calendrier_tard) - 1:
            is_last_line = True
        
        # Affichage de l'identifiant de la tâche
        cell1 = print_schedule_line(str(task), (size1 - len(str(task))))
        
        # Affichage de la date au plus tot de la tâche
        early_date = str(calendrier_tot[task])
        cell2 = print_schedule_line(early_date, size2 - len(early_date))
        
        # Affichage de la date au plus tard de la tâche
        late_date = str(calendrier_tard[task])
        cell3 = print_schedule_line(late_date, size3 - len(late_date))
        
        # Affichage de la ligne
        if is_last_line:
            print(f"{shift}|{COLORS.UNDERLINE} {cell1} | {cell2} | {cell3}{COLORS.END}|")
        else:
            print(f"{shift}| {cell1} | {cell2} | {cell3}|")
    print()


def print_marges(marge_totale, marge_libre):
    printTitle("\n* Marges :\n")
    
    if len(marge_totale) != len(marge_libre):
        raise "Error: in print_schedules: Verifiez que les marges totales et les marges libres sont de meme " \
              "tailles"
    
    # Espacement avant chaque ligne
    shift = "  "
    
    # Titres des colonnes
    title1 = "Taches"
    title2 = "Marges Totales"
    title3 = "Marges Libres"
    
    # Tailles des colonnes
    size1 = len(title1)
    size2 = len(title2)
    size3 = len(title3) + 1
    
    # Affichage des titres
    print(shift, end="")
    print(f" {COLORS.UNDERLINE}{COLORS.BOLD} {title1}   {title2}   {title3} {COLORS.END}")
    
    # Variable pour indiquer si on est sur la dernière ligne
    is_last_line = False
    
    # Parcours des tâches dans l'ordre de la liste des identifiants
    for task in range(len(marge_totale)):
        if task == len(marge_totale) - 1:
            is_last_line = True
        
        # Affichage de l'identifiant de la tâche
        cell1 = print_schedule_line(str(task), (size1 - len(str(task))))
        
        # Affichage de la date au plus tot de la tâche
        early_date = str(marge_totale[task])
        cell2 = print_schedule_line(early_date, size2 - len(early_date))
        
        # Affichage de la date au plus tard de la tâche
        late_date = str(marge_libre[task])
        cell3 = print_schedule_line(late_date, size3 - len(late_date))
        
        # Affichage de la ligne
        if is_last_line:
            print(f"{shift}|{COLORS.UNDERLINE} {cell1} | {cell2} | {cell3}{COLORS.END}|")
        else:
            print(f"{shift}| {cell1} | {cell2} | {cell3}|")
    print()


class COLORS:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printNodes(nodes):
    for node_id in nodes:
        print(node_id, end=" ")
    print()


def printWarning(string):
    print(f"{COLORS.WARNING}Warning: {COLORS.END}{string}")


def printTitle(string, end="\n"):
    print(f"{COLORS.BOLD}{COLORS.UNDERLINE}{string}{COLORS.END}", end=end)


def printBold(string):
    print(f"{COLORS.BOLD}{string}{COLORS.END}")


def printError(string):
    print(f"\n{COLORS.FAIL}ERROR: {COLORS.END}{string}")


def printGreen(string, end="\n"):
    print(f"{COLORS.GREEN}>{COLORS.END} {string}", end=end)


def clear_output():
    for i in range(10):
        print()
    print("\033[H\033[2J")


def printShift(string, end="\n"):
    print(SHIFT + string, end=end)
