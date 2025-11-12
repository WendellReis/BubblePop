import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import json
import copy
import src.utils.sucessor as sucessor
import src.utils.action as action
import globals

class GameStateTree:
    """
    Representa uma árvore (ou grafo) de estados do jogo.
    Cada aresta contém uma ação no formato [op, data].
    """
    def __init__(self, game):
        self.G = nx.DiGraph()
        self.game = game
        self.current_state = copy.deepcopy(game.get_state())
        self.current_id = self.state_id(self.current_state)
        self.G.add_node(self.current_id, state=copy.deepcopy(self.current_state))
        self.expand_state()

    def state_id(self, state):
        state_copy = copy.deepcopy(state)
        state_str = json.dumps(state_copy, sort_keys=True)
        return hashlib.md5(state_str.encode()).hexdigest()
        
    def expand_state(self, parent_id=None):
        """Expande o nó parent_id gerando filhos a partir do estado armazenado no nó pai."""
        if parent_id is None:
            parent_id = self.current_id

        if parent_id not in self.G:
            print(f"[WARN] parent_id {parent_id} ausente — adicionando com current_state.")
            self.G.add_node(parent_id, state=copy.deepcopy(self.current_state))

        parent_node_data = self.G.nodes[parent_id]
        parent_state = parent_node_data.get("state")
        if parent_state is None:
            print(f"[WARN] parent_id {parent_id} sem atributo 'state' — usando current_state como fallback.")
            parent_state = copy.deepcopy(self.current_state)
            self.G.nodes[parent_id]["state"] = parent_state
        else:
            parent_state = copy.deepcopy(parent_state)

        possible_states = self.possible_states(parent_state)

        for child_state in possible_states:
            if not isinstance(child_state, dict):
                print(f"[WARN] possible_states retornou item inválido: {child_state!r} — pulando.")
                continue

            child_id = self.state_id(child_state)

            if child_id not in self.G:
                self.G.add_node(child_id, state=copy.deepcopy(child_state))
            else:
                if "state" not in self.G.nodes[child_id]:
                    print(f"[WARN] Corrigindo nó filho {child_id} sem 'state'.")
                    self.G.nodes[child_id]["state"] = copy.deepcopy(child_state)

            if parent_id not in self.G:
                self.G.add_node(parent_id, state=copy.deepcopy(self.current_state))

            self.G.add_edge(parent_id, child_id)

    def go_to_state(self, op, data):
        next_state = action.EXECUTE(self.game.get_state(), op, data)
        self.current_state = copy.deepcopy(next_state)
        self.current_id = self.state_id(self.current_state)

        if self.current_id not in self.G:
            self.G.add_node(self.current_id, state=copy.deepcopy(self.current_state))
        else:
            self.G.nodes[self.current_id]["state"] = copy.deepcopy(self.current_state)

        self.expand_state(self.current_id)

        self.game.set_state(copy.deepcopy(next_state))

    def possible_states(self, state=None):
        """Retorna a lista de estados filhos gerados a partir de 'state'."""
        if state is None:
            state = copy.deepcopy(self.current_state)
        else:
            state = copy.deepcopy(state)

        states = []
        actions = sucessor.GET(state)
        if not isinstance(actions, (list, tuple)):
            print(f"[WARN] sucessor.GET retornou algo inesperado: {actions!r}")
            return states

        for act in actions:
            try:
                op, data = act
            except Exception:
                #print(f"[WARN] ação inválida em sucessor.GET: {act!r}")
                continue

            # chama EXECUTE com uma cópia para evitar mutação do 'state' original
            try:
                child_state = action.EXECUTE(copy.deepcopy(state), op, data)
            except Exception as e:
                print(f"[ERROR] action.EXECUTE falhou para op={op}, data={data}: {e}")
                continue

            if not isinstance(child_state, dict):
                print(f"[WARN] action.EXECUTE retornou não-dict: {child_state!r}")
                continue

            states.append(child_state)
        
        return states

    def get_parent(self, state_id):
        return next(self.G.predecessors(state_id), None)

    def get_children(self, state_id):
        return list(self.G.successors(state_id))
    
    def got_to_previous(self):
        parent_id = self.get_parent(self.current_id)

        if parent_id is not None:
            previous_state = self.G.nodes[parent_id]["state"]
            self.game.set_state(previous_state)
            self.current_state = previous_state
            self.current_id = parent_id

    def draw_graph(self):
        # layout
        try:
            pos = nx.nx_agraph.graphviz_layout(self.G, prog="dot")
        except Exception:
            pos = nx.spring_layout(self.G, seed=42)

        colors = []
        labels = {}

        '''
        # debug: imprime nós com e sem 'state'
        print("\n=== DEBUG NODES ===")
        for node_id, data in self.G.nodes(data=True):
            if "state" not in data:
                print(f"[ERR] Nó {node_id} sem 'state'! data={data}")
            else:
                s = data["state"]
                print(f"OK {node_id[:8]} turn={s.get('turn')} cur={s.get('current_state')}")
        print("===================\n")
        '''

        for n in self.G.nodes:
            node_data = self.G.nodes[n]
            state = node_data.get("state")
            if state is None:
                labels[n] = "?"
                colors.append("gray")
                continue

            labels[n] = f'{globals.STR_STATES.get(state.get("current_state"), str(state.get("current_state")))}'
            if self.state_id(state) == self.current_id:
                colors.append("green")
            else:
                if state.get('turn_power') == -1:
                    colors.append("red" if state.get("turn") == 0 else "blue")
                else:
                    colors.append("red" if state.get("turn_power") == 0 else "blue")

        nx.draw_networkx_edges(self.G, pos, arrows=True, alpha=0.5)
        nx.draw_networkx_nodes(self.G, pos, node_color=colors, node_size=900, edgecolors="black")
        nx.draw_networkx_labels(self.G, pos, labels, font_color="white", font_weight="bold", font_size=8)

        plt.axis("off")
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(10)
        plt.close()
