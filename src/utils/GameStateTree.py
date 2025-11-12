import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import json
import copy
import src.utils.sucessor as sucessor
import src.utils.action as action


class GameStateTree:
    """
    Representa uma árvore (ou grafo) de estados do jogo.
    Cada aresta contém uma ação no formato [op, data].
    """
    def __init__(self,game):
        self.G = nx.DiGraph()
        self.game = game
        self.current_state = game.get_state()
        self.current_state_id = self.state_id(self.current_state)

    def state_id(self, state):
        #state_copy = copy.deepcopy(state)
        #state_str = json.dumps(state_copy, sort_keys=True)
        #return hashlib.md5(state_str.encode()).hexdigest()

        state_str = str(sorted(state.items())).encode()
        return hashlib.md5(state_str).hexdigest()
        
    def expand_state(self,parent_id=None):
        if parent_id is None:
            parent_id = self.current_state_id

        possible_states = self.game.possible_states()
        for child_state in possible_states:
            child_id = self.state_id(child_state)

            if child_id not in self.G:
                self.G.add_node(child_id,child_state)
            self.G.add_edge(parent_id, child_id)

    def go_to_state(self,op,data):
        next_state = action.EXECUTE(self.game.get_state(),op,data)
        self.game.set_state(next_state)

    def draw_graph(self):
        pos = nx.nx_agraph.graphviz_layout(self.G, prog="dot")
        colors = [
            "red" if self.G.nodes[n]["player"] == 0 else "blue"
            for n in self.G.nodes
        ]
        nx.draw(self.G, pos, with_labels=False, node_color=colors, node_size=700, arrows=True)
        nx.draw_networkx_labels(self.G, pos, {self.current_id: "★"}, font_color="black", font_weight="bold")
        plt.show()
