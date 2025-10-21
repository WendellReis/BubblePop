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
    elif s == globals.STATE_SWAP_BUBBLEES:
        return SWAP_BUBBLESS(state,data)
    elif s == globals.STATE_DROP_BUBBLEES:
        return DROP_BUBBLEES(state,data)
    
    print("ERRO action.EXECUTE")

def NAVIGATE(state,data):
    state["current_state"] = data
    return state

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
            return NAVIGATE(state,globals.STATE_SWAP_BUBBLEES)
        return state
    print("ERRO action.SETUP_SKY: Parametro 'action' invalido!")

def SWAP_BUBBLESS(state,data):
    c1 = data[0]
    c2 = data[1]
    aux = state["sky"][c1[0]][c1[1]]
    state["sky"][c1[0]][c1[1]] = state["sky"][c2[0]][c2[1]]
    state["sky"][c2[0]][c2[1]] = aux
    state["current_state"] = globals.STATE_DROP_BUBBLEES
    return state

def DROP_BUBBLEES(state,data):
    turn = state["turn"]
    planet = state["planet"][turn]
    sky = state["sky"]
    data.sort()
    for x,y in data:
        color = sky[x][y]
        sky[x][y] = ''

        x = 0
        while x < 6 and planet[x][y] in globals.COLORS:
            x+=1
        planet[x][y] = color
    
    state["current_state"] = globals.STATE_CHECK_MATCHES
    return state
    