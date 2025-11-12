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
        self.game = game
        self.graph = nx.DiGraph()
        self.current_state = game.get_state()

    def state_id(self, state):
        state_copy = copy.deepcopy(state)
        state_str = json.dumps(state_copy, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_state(self, state, parent_state=None, act=None):
        pass

    def expand_state(self, state):
        pass

    def draw_graph(self):
        pos = nx.nx_agraph.graphviz_layout(self.G, prog="dot")
        colors = [
            "red" if self.G.nodes[n]["player"] == 0 else "blue"
            for n in self.G.nodes
        ]
        nx.draw(self.G, pos, with_labels=False, node_color=colors, node_size=700, arrows=True)
        nx.draw_networkx_labels(self.G, pos, {self.current_id: "★"}, font_color="black", font_weight="bold")
        plt.show()
