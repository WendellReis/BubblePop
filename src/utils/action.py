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
    elif action == "CHECK_WIN":
        return CHECK_WIN(state)
    
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

def CHECK_WIN(state):
    for w in [0,1]:
        planet = state.get('planet')[w]
        for i in range[4,5]:
            for j in range(5):
                if planet[i][j] in globals.COLORS:
                    state['winner'] = w
                    state['current_state'] = globals.STATE_ENDGAME
                    return state

    if state.get('bubblees_in_bag') == 0:
        s0 = state.get('score')[0]
        s1 = state.get('score')[1]

        if s0 > s1:
            state['winner'] = 0
        elif s1 > s0:
            state['winner'] = 1
        else:
            state['winner'] = -1
        state['current_state'] = globals.STATE_ENDGAME
        return state
    return state

    
def CHECK_MATCHES(state):
    if state.get('turn_power') == -1:
        turn = state.get('turn')
        p = state.get('planet')[turn]

