# Arquivo contendo as ações do jogo
import globals

def EXECUTE(state,action,data=None):
    if action == "NAVIGATE":
        return NAVIGATE(state,data)

    s = state["current_state"]

    if s == globals.STATE_SETUP_SKY:
        if data is None:
            return SETUP_SKY(state,action)
        return SETUP_SKY(state,action,data)
    print("ERRO action.EXECUTE")

def SETUP_SKY(state,action,data=None):
    if action == "GENERATE_BUBBLEE":
        state["bag_color"] = data
        state["bubblees_in_bag"]-=1
        return state
    elif action == "SETUP":
        x,y = data
        state["sky"][x][y] = state["bag_color"]
        state["bag_color"] = ""
        
        full = True
        for j in range(0,5):
            if state['sky'][0][j] not in globals.COLORS or state['sky'][1][j] not in globals.COLORS:
                full = False
                break
        if full:
            return NAVIGATE(state,[globals.STATE_SWAP_BUBBLEES,False])
        return state
    print("ERRO action.SETUP_SKY: Parametro 'action' invalido!")

def NAVIGATE(state,data):
    # data[1] decide sobre a mudança de turno
    state["current_state"] = data[0]
    if data[1]:
        state["turn"] = (state["turn"]+1)%2
    return state