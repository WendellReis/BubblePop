import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import json
import src.utils.sucessor as sucessor
import src.utils.action as action


class GameStateGraph:
    """
    Representa uma árvore (ou grafo) de estados do jogo.
    Cada aresta contém uma ação no formato [op, data].
    """
    def __init__(self):
        self.graph = nx.DiGraph()  # grafo direcionado de estados

    def state_id(self, state):
        """Gera um ID único para cada estado (hash MD5 do dicionário)."""
        state_str = json.dumps(state, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_state(self, state, parent_state=None, act=None):
        """Adiciona um estado e (se houver) a ligação com o pai via ação."""
        sid = self.state_id(state)
        self.graph.add_node(sid, label=str(state))

        if parent_state is not None and act is not None:
            parent_id = self.state_id(parent_state)
            
            # Garantir que a ação é armazenada no formato [op, data]
            if not isinstance(act, list) or len(act) != 2:
                raise ValueError(f"Ação inválida: {act}. Esperado formato [op, data].")
            
            op, data = act
            label = f"[{op}, {data}]"
            self.graph.add_edge(parent_id, sid, label=label)

    def expand_state(self, state):
        """Expande o estado com todas as ações possíveis."""
        for act in sucessor.sucessora(state):
            if not isinstance(act, list) or len(act) != 2:
                raise ValueError(f"Ação inválida retornada por sucessora: {act}")
            
            next_state = action.EXECUTE(state, act)
            self.add_state(next_state, parent_state=state, act=act)

    def draw_graph(self):
        """Desenha o grafo de estados."""
        pos = nx.spring_layout(self.graph, seed=42)
        edge_labels = nx.get_edge_attributes(self.graph, 'label')

        plt.figure(figsize=(12, 8))
        nx.draw(
            self.graph,
            pos,
            with_labels=False,
            node_color='lightblue',
            node_size=1200,
            arrows=True,
        )
        # Exibe apenas os primeiros 5 caracteres do hash para clareza
        nx.draw_networkx_labels(self.graph, pos, {n: n[:5] for n in self.graph.nodes()})
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        plt.title("Grafo de Estados do Jogo")
        plt.show()
