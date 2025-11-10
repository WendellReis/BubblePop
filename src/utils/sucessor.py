import globals

def setup_sky(state):
    actions = []
    
    count = 0
    bubblees_in_bag = state.get('bubblees_in_bag')
    sky = state.get('sky')

    rows = len(sky)
    cols = len(sky[0]) if rows > 0 else 0
    for j in range(min(5, cols)):
        if rows > 0 and sky[0][j] in globals.COLORS:
            count += 1
        if rows > 1 and sky[1][j] in globals.COLORS:
            count += 1

    if count > bubblees_in_bag:
        return [None]
    
    if count == 12: # Céu completo
        return ["NAVIGATE",globals.STATE_SWAP_BUBBLEES]
    
    if state.get('bag_color') not in globals.COLORS:
        for c in globals.COLORS: # Todos os resultados para o sorteio do bubblee
            actions.append(["GENERATE_BUBBLEE",c]) 
    else:
        for j in range(5):
            if sky[0][j] not in globals.COLORS:
                actions.append(["SETUP",[0,j]])
            if sky[1][j] not in globals.COLORS:
                actions.append(["SETUP",[1,j]])
    
    return actions

def endgame(state):
    return [None]

HANDLER = {
    globals.STATE_SETUP_SKY: setup_sky,
    globals.STATE_ENDGAME: endgame,
}


def GET(state):
    current_state = state.get('current_state')
    handler = HANDLER.get(current_state)
    if handler is None:
        return [None]
    return handler(state)
