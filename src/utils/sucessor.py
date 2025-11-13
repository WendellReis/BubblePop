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
        return [["CHECK_WIN",-1]]
    
    if count == 12: # Céu completo
        return [["NAVIGATE",globals.STATE_SWAP_BUBBLEES]]
    
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

def swap_bubblees(state):
    actions = [["NAVIGATE",globals.STATE_DROP_BUBBLEES]]

    sky = state.get('sky')
    cols = len(sky[0])
    for j in range(cols):
        if sky[0][j] in globals.COLORS and sky[1][j] in globals.COLORS:
            actions.append(["SWAP_BUBBLEES",[[0,j],[1,j]]])

    for j in range(cols-1):
        if sky[0][j] in globals.COLORS and sky[0][j+1] in globals.COLORS:
            actions.append(["SWAP_BUBBLEES",[[0,j],[0,j+1]]])
        if sky[1][j] in globals.COLORS and sky[1][j+1] in globals.COLORS:
            actions.append(["SWAP_BUBBLEES",[[1,j],[1,j+1]]])

    return actions

def drop_bubblees(state):
    actions = []

    turn = state.get('turn')
    sky = state.get('sky')
    cols = len(sky[0])
    for j in range(cols):
        if sky[0][j] in globals.COLORS and sky[1][j] in globals.COLORS:
            actions.append(["DROP_BUBBLEES",[[0,j],[1,j]]])

    for j in range(cols-1):
        if sky[turn][j] in globals.COLORS and sky[turn][j+1] in globals.COLORS:
            actions.append(["DROP_BUBBLEES",[[turn,j],[turn,j+1]]])

    return actions

def choose_power(state):
    actions = []

    stack = state.get('power_stack')

    if len(stack) == 0:
        return [["CHECK_WIN",-1]]
    
    powers = stack[-1][1]
    for p in powers:
        actions.append(["ACCEPT_POWER",p])
        actions.append(["REJECT_POWER",p])

    return actions
    
def check_macthes(state):
    return [["CHECK_MATCHES",-1]]

def check_win(state):
    return [["CHECK_WIN",-1]]

def power_yellow(state):
    actions = []

    turn_power = state.get('turn_power')
    p = state.get('planet')[turn_power]

    rows = len(p)
    col = len(p[0])
    for j in range(col):
        i = rows-1
        while i >= 0:
            if p[i][j] in globals.COLORS:
                actions.append(["POWER_YELLOW",[i,j]])
                break
            i-=1

    return actions

def swap_bubblees_power(state,power):
    actions = []

    if power == "RED":
        idx = (state.get('turn_power')+1)%2
    elif power == "GREEN":
        idx = state.get('turn_power')

    p = state.get('planet')[idx]
    rows = len(p)
    col = len(p[0])

    for i in range(rows-1):
        for j in range(col):
            if p[i][j] in globals.COLORS and p[i+1][j] in globals.COLORS:
                actions.append([f"POWER_{power}",[[i,j],[i+1,j]]])

    for i in range(rows):
        for j in range(col-1):
            if p[i][j] in globals.COLORS and p[i][j+1] in globals.COLORS:
                actions.append([f"POWER_{power}",[[i,j],[i,j+1]]])

    return actions

def power_red(state):
    return swap_bubblees_power(state,"RED")

def power_green(state):
    return swap_bubblees_power(state,"GREEN")

def power_blue(state):
    actions = []

    turn_power = state.get('turn_power')
    p = state.get('planet')[(turn_power+1)%2]
    full = True
    col = len(p[0])
    for j in range(col):
        if p[3][j] not in globals.COLORS:
            full = False
            break

    sky = state.get('sky')
    col = len(sky[0])
    for j in range(col):
        if sky[(turn_power+1)%2][j] in globals.COLORS:
            if full or p[3][j] not in globals.COLORS:
                actions.append(["POWER_BLUE",[(turn_power+1)%2,j]])
    
    return actions

def is_free_bubblee(p,i,j):
    if p[i][j] not in globals.COLORS:
        return False
    i+=1
    while i < 6:
        if p[i][j] in globals.COLORS:
            return False
        i+=1
    return True

def power_purple(state):
    actions = []
    
    turn_power = state.get('turn_power')
    p1 = state.get('planet')[turn_power]
    p2 = state.get('planet')[(turn_power+1)%2]

    full = True
    col = len(p2[0])
    for j in range(col):
        if p2[3][j] not in globals.COLORS:
            full=False
            break

    rows = len(p1)
    for i in range(rows):
        for j in range(col):
            if is_free_bubblee(p1,i,j) and (full or p2[3][j] not in globals.COLORS): 
                actions.append(["POWER_PURPLE",[i,j]])

    return actions

HANDLER = {
    globals.STATE_SETUP_SKY: setup_sky,
    globals.STATE_SWAP_BUBBLEES: swap_bubblees,
    globals.STATE_DROP_BUBBLEES: drop_bubblees,
    globals.STATE_CHECK_MATCHES: check_macthes,
    globals.STATE_CHOOSE_POWER: choose_power,
    globals.STATE_POWER_YELLOW: power_yellow,
    globals.STATE_POWER_RED: power_red,
    globals.STATE_POWER_GREEN: power_green,
    globals.STATE_POWER_BLUE: power_blue,
    globals.STATE_POWER_PURPLE: power_purple,
    globals.STATE_CHECK_WIN: check_win,
}

def GET(state):
    current_state = state.get('current_state')
    handler = HANDLER.get(current_state)
    if handler is None:
        return [["NOTHING",-1]]
    return handler(state)
