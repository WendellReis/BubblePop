import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import json
import random

# ======================================================
# Funções auxiliares para gerar IDs e manipular estados
# ======================================================

def state_id(state):
    """Gera um ID único para cada estado (hash MD5 do dicionário)."""
    state_str = json.dumps(state, sort_keys=True)
    return hashlib.md5(state_str.encode()).hexdigest()

def add_state(graph, state, parent_state=None, action=None):
    """Adiciona um estado e a ligação com o estado pai (se houver)."""
    sid = state_id(state)
    graph.add_node(sid, label=str(state))
    
    if parent_state is not None and action is not None:
        parent_id = state_id(parent_state)
        graph.add_edge(parent_id, sid, label=str(action))

def expand_state(graph, state, sucessora, action_execute):
    """Expande o estado com todas as ações possíveis."""
    for action in sucessora(state):
        next_state = action_execute(state, action)
        add_state(graph, next_state, parent_state=state, action=action)

# ======================================================
# Funções de exemplo do jogo (simulação simplificada)
# ======================================================

def sucessora(state):
    """Gera 2 ou 3 ações possíveis de exemplo."""
    num_actions = random.randint(2, 3)
    return [f"Ação_{i}" for i in range(num_actions)]

def action_execute(state, action):
    """Retorna um novo estado alterando turno e pontuação."""
    new_state = dict(state)  # copia o estado
    new_state["turn"] = 1 - state["turn"]
    new_state["score"][new_state["turn"]] += random.randint(1, 5)
    new_state["step"] += 1
    return new_state

# ======================================================
# Função para desenhar o grafo
# ======================================================

def draw_graph(graph):
    pos = nx.spring_layout(graph, seed=42)
    edge_labels = nx.get_edge_attributes(graph, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=False, node_color='lightblue', node_size=1200, arrows=True)
    nx.draw_networkx_labels(graph, pos, {n: n[:5] for n in graph.nodes()})
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Árvore de Estados do Jogo")
    plt.show()

# ======================================================
# Simulação principal
# ======================================================

# Estado inicial do "jogo"
initial_state = {"turn": 0, "score": [0, 0], "step": 0}

# Cria o grafo
G = nx.DiGraph()
add_state(G, initial_state)

# Expande 3 níveis para simular jogadas
current_states = [initial_state]
for depth in range(3):  # 3 níveis de profundidade
    next_states = []
    for state in current_states:
        expand_state(G, state, sucessora, action_execute)
        next_states.extend([action_execute(state, a) for a in sucessora(state)])
    current_states = next_states

# Mostra o grafo final
draw_graph(G)
