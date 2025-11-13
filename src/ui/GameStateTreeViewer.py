import matplotlib.pyplot as plt
import networkx as nx
import globals

class GameStateTreeViewer:
    """Exibe e salva o grafo de estados do jogo."""

    @staticmethod
    def show(tree, filename="game_tree.png"):
        plt.figure(figsize=(18, 14))
        try:
            pos = nx.nx_agraph.graphviz_layout(
                tree.G,
                prog="dot",
                args="-Grankdir=TB -Gnodesep=0.5 -Granksep=2.0"
            )
        except Exception:
            pos = nx.spring_layout(tree.G, k=0.8, iterations=200, seed=42)


        colors, labels = [], {}
        for n, data in tree.G.nodes(data=True):
            state = data.get("state")
            if not state:
                labels[n] = "?"
                colors.append("gray")
                continue

            labels[n] = f'{globals.STR_STATES.get(state.get("current_state"), str(state.get("current_state")))}'
            if tree.state_id(state) == tree.current_id:
                colors.append("green")
            else:
                aux = True
                if state.get('current_state') == globals.STATE_SETUP_SKY and state.get('bag_color') not in globals.COLORS:
                    sky = state.get('sky')
                    col = len(sky[0])
                    for j in range(col):
                        if sky[0][j] not in globals.COLORS or sky[1][j] not in globals.COLORS:
                            colors.append("orange")
                            aux = False
                            break
                if aux:
                    if state.get('turn_power') == -1:
                        colors.append("red" if state.get("turn") == 0 else "blue")
                    else:
                        colors.append("red" if state.get("turn_power") == 0 else "blue")

        nx.draw_networkx_edges(tree.G, pos, arrows=True, alpha=0.5)
        nx.draw_networkx_nodes(tree.G, pos, node_color=colors, node_size=900, edgecolors="black")
        nx.draw_networkx_labels(tree.G, pos, labels, font_color="white", font_weight="bold", font_size=8)

        plt.axis("off")
        plt.tight_layout()

        # salva imagem
        #plt.savefig(filename, dpi=300, bbox_inches="tight")

        # mostra de forma leve
        plt.show(block=False)
        plt.pause(5)
        plt.close()