# Arquivo contendo as ações do jogo
import globals

def EXECUTE(state,action,data=None):
    s = state["current_state"]

    if s == globals.STATE_SETUP_SKY:
        if data is None:
            return SETUP_SKY(state,action)
        return SETUP_SKY(state,action,data)

def SETUP_SKY(state,action,data=None):
    if action == "ENDGAME":
        state["current_state"] = globals.STATE_ENDGAME
    elif action == "CHECKWIN":
        state["current_state"] = globals.STATE_CHECK_WIN
    elif action == "SETUP":
        x,y = data [0]
        state["sky"][x][y] = data[1]
    return state