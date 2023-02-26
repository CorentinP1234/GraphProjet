def read_constraints_table(file: str):
    # Initialize the tasks, all_nodes_ids, and starting_nodes_ids lists
    tasks: list(Task) = []               # list of Task objects
    # list of all node IDs (task numbers) in the graph, initialized with the "alpha" node
    node_ids: list(int) = [-1]
    # list of node IDs that have no predecessors (i.e. starting nodes)
    starting_nodes_ids: list(int) = []

    with open(file, 'r') as f:

        print(f"* Creation du graphe d'ordonnancement {file[:-5]}:")

        # 0. Read the input file and create Task objects from each line

        for line in f.read().splitlines():
            # Extract task number, duration, and predecessors from the line
            task_num, duration, *predecessors = map(int, line.split())

            # Check if the input is valid
            if not (task_num > -1 and duration > 0 and all(x > 0 for x in predecessors)):
                raise("Error: this table is not valid.")

            # If the task has no predecessors, mark it as a starting node
            if not predecessors:
                if task_num in starting_nodes_ids:
                    raise(f"Error: reading task {task_num} again")
                starting_nodes_ids.append(task_num)

            # Create a new Task object and add it to the tasks list
            tasks.append(Task(task_num, duration, predecessors))

            # Add the task number to the all_nodes_ids set
            node_ids.append(task_num)

        # Add the "omega" node ID to the all_nodes_ids set
        node_ids.append(len(node_ids))

        # 1. Create the edges list

        edges: list(Edge) = []

        # Add the "alpha" edges (-1 -> starting nodes) to the edges list
        for starting_node_id in starting_nodes_ids:
            edges.append(Edge(-1, starting_node_id, 0))

        # Add the other edges (node -> successors) to the edges list
        for node_id in sorted(node_ids)[0:-1]:
            # Check if the node has successors
            is_a_final_node = True
            for task in tasks:
                if node_id in task.pred and node_id != task.id:
                    # If the node has successors, add the edges to the edges list
                    is_a_final_node = False
                    edges.append(Edge(node_id, task.id, tasks[node_id-2].dur))

            # If the node has no successors, add the edge to the "omega" node to the edges list
            if is_a_final_node:
                edges.append(
                    Edge(node_id, len(node_ids)-2, tasks[node_id-1].dur))

        print(f"{len(node_ids)} sommets")
        print(f"{len(edges)} arcs")
        Edge.print(edges)

        return Table(node_ids, edges)
