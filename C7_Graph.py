from C7_Utils import *


class Graph:
    # self.adj_list[from_node][to_node] = self.duration_of[from_node]
    def __init__(self, name):
        self.name = name
        self.predecessor_of = {}
        self.successor_of = {0: set()}
        self.duration_of = {0: 0}
        self.node_ids = {0}
        self.number_of_edges = 0
        self.omega_node_id = None
        self.adjacency_matrix = None
        self.i = 0
    
    def add_node(self, node_id, duration):
        """Add a node_id (int) to the to set of ids node_ids"""
        if node_id in self.node_ids:
            print(f"{COLORS.WARNING}Warning{COLORS.ENDC}: Tache {node_id} a deja été ajouté")
        self.node_ids.add(node_id)
        if duration:
            if node_id in self.duration_of:
                print(f"Warning : Tache {node_id} avait pour durée {duration[node_id]}\
                         et va être écrasé par {duration}")
            self.duration_of[node_id] = duration
    
    def get_number_of_nodes(self):
        return len(self.node_ids)
    
    def get_number_of_edges(self):
        return self.number_of_edges
    
    def get_successors(self, node_id) -> tuple[int]:
        # Return a set of successors or an empty set
        return self.successor_of.get(node_id, set())
    
    def get_predecessors(self, node_id):
        # Return a set of predecessors or an empty set
        return self.predecessor_of.get(node_id, set())
    
    def add_omega_node(self):
        # Add the last node and no duration is set
        self.omega_node_id = len(self.node_ids)
        self.add_node(self.omega_node_id, None)
    
    def add_edge(self, from_node, to_node):
        """Add an edge by updating maps of predecessors and successors, increment the number of edges"""
        # Update set of predecessors
        if to_node not in self.predecessor_of:
            self.predecessor_of[to_node] = set()
        self.predecessor_of[to_node].add(from_node)
        
        # Update set of successors
        if from_node not in self.successor_of:
            self.successor_of[from_node] = set()
        self.successor_of[from_node].add(to_node)
        
        # Update the number of edges
        self.number_of_edges += 1
    
    def add_edges(self, predecessors, node_id):
        """Add edges from each predecessor in the list of predecessors to the node with node_id"""
        
        # If the task has predecessors, add edges pred -> task_num
        if predecessors:
            for pred in predecessors:
                self.add_edge(pred, node_id)
        
        # If not, add an edge 'alpha' -> task_num
        else:
            self.add_edge(0, node_id)
    
    def add_omega_edges(self):
        nodes_with_ex_edge = self.successor_of.keys()
        for node_id in self.node_ids - {self.omega_node_id}:
            if node_id not in nodes_with_ex_edge:
                self.add_edge(node_id, self.omega_node_id)
    
    def get_nodes_with_no_predecessors2(self, ignore=None):
        if ignore is None:
            ignore = set()
        res = self.node_ids - (set(self.predecessor_of.keys()).union(ignore))
        if self.i == 1:
            print()
            print(self.node_ids)
            print(self.predecessor_of.keys())
            print(ignore)
            print(f"no pred : {res}")
            exit()
        else:
            self.i += 1
        return res
    
    def get_nodes_with_no_predecessors(self, ignore=None):
        if ignore is None:
            ignore = set()
        predOf = self.predecessor_of.copy()
        
        # Remove Ignored nodes
        nodes_with_no_pred = set()
        for node in predOf.keys():
            predOf[node] -= ignore
            if not predOf[node]:
                nodes_with_no_pred.add(node)
        
        if not nodes_with_no_pred:
            nodes_with_no_pred = {0}
        
        return nodes_with_no_pred - ignore
    
    def print(self):
        print(f"{COLORS.UNDERLINE}Graphe d'ordonnancement de " + self.name + COLORS.ENDC)
        print(f" {len(self.node_ids)} sommets")
        print(f" {self.number_of_edges} arcs")
        for from_node, to_nodes in sorted(self.successor_of.items()):
            for to_node in to_nodes:
                duration = self.duration_of[from_node]
                print(f" {from_node} -> {to_node} = {duration}")
        print()
    
    
    def get_adjacency_matrix(self) -> list:
        num_nodes = self.get_number_of_nodes()
        adjacency_matrix = [['.'] * num_nodes for _ in range(num_nodes)]
        for from_node in self.node_ids:
            for to_node in self.get_successors(from_node):
                adjacency_matrix[from_node][to_node] = self.duration_of[from_node]
        return adjacency_matrix
    
    # def add_successor(self, node_id, succ):
    #     if node_id not in self.successor_of:
    #         self.successor_of[node_id] = set()
    #     self.successor_of[node_id].add(succ)
    
    # def add_predecessor(self, node_id, pred):
    #     if node_id not in self.predecessor_of:
    #         self.predecessor_of[node_id] = set()
    #     self.predecessor_of[node_id].add(pred)
