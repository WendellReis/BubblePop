# Arquivo contendo as ações do jogo
import globals

def EXECUTE(state,action,data=None):
    s = state["current_state"]

    if s == globals.STATE_SETUP_SKY:
        if data is None:
            return SETUP_SKY(state,action)
        return SETUP_SKY(state,action,data)

def SETUP_SKY(state,action,data=None):
    if action == "SWAP_BUBBLESES":
        state["current_state"] = globals.STATE_SWAP_BUBBLEES
    elif action == "CHECKWIN":
        state["current_state"] = globals.STATE_CHECK_WIN
    elif action == "GENERATE_BUBBLEE":
        state["bag_color"] = data
        state["bubblees_in_bag"]-=1
    elif action == "SETUP":
        x,y = data
        state["sky"][x][y] = state["bag_color"]
        state["bag_color"] = ""
    return state