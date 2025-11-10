# Arquivo contendo as ações do jogo
import globals

def EXECUTE(state,action,data=None):
    if action == "NAVIGATE":
        return NAVIGATE(state,data)
    
    s = state["current_state"]

    if action == "CHECK_WIN":
        return CHECK_WIN(state)
    elif action == "CHECK_MATCHES":
        return CHECK_MATCHES(state)
    elif action == "ACCEPT_POWER":
        return ACCEPT_POWER(state,data)
    elif action == "REJECT_POWER":
        return REJECT_POWER(state,data)
    elif action == "POWER_YELLOW":
        return POWER_YELLOW(state,data)
    elif action == "POWER_RED":
        return POWER_RED(state,data)
    elif action == "POWER_GREEN":
        return POWER_GREEN(state,data)
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
        x = 4
        while x >= 0 and planet[x][y] not in globals.COLORS:
            x-=1
        planet[x+1][y] = color
    
    state["current_state"] = globals.STATE_CHECK_MATCHES
    return state

def CHECK_WIN(state):
    for w in [0,1]:
        planet = state.get('planet')[w]
        for i in range(4,5):
            for j in range(5):
                if planet[i][j] in globals.COLORS:
                    state['winner'] = (w+1)%2
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
    
    if len(state.get('power_stack')) == 0:
        state['current_state'] = globals.STATE_SETUP_SKY
        state['turn_power'] = -1
        state['turn'] = (state.get('turn')+1)%2
    else:
        state['current_state'] = globals.STATE_CHOOSE_POWER
    return state

def dfs(p,color,i,j):
    p[i][j] = ' '
    points = 1

    if i + 1 < 6 and p[i+1][j] == color:
        points+=dfs(p,color,i+1,j)
    if i - 1 >= 0 and p[i-1][j] == color:
        points+=dfs(p,color,i-1,j)
    if j + 1 < 5 and p[i][j+1] == color:
        points+=dfs(p,color,i,j+1)
    if j - 1 >= 0 and p[i][j-1] == color:
        points+=dfs(p,color[j-1])
    
    return points

def drop_free_bubblees(p):
    res = False
    for j in range(5):
        i = 0

        aux = True
        while aux:
            aux = False
            for i in range(1,6):
                if p[i][j] in globals.COLORS and p[i-1][j] not in globals.COLORS:
                    p[i-1][j] = p[i][j]
                    p[i][j] = ' '
                    aux = True
                    res = True
    return res

def CHECK_MATCHES(state):
    if state.get('turn_power') == -1 or state.get('current_state') in [globals.STATE_POWER_GREEN, globals.STATE_POWER_YELLOW]:
        turn = state.get('turn')
    else:
        turn = (state.get('turn')+1)%2

    p = state.get('planet')[turn]
    stack = []

    while True:
        for i in range(0,6):
            for j in range(0,3):
                color = p[i][j]
                if color in globals.COLORS and color != 'x' and color == p[i][j+1] and color == p[i][j+2]:
                    points = dfs(p,color,i,j)

                    if points:
                        state['score'][turn] += points
                        if color not in stack: # Não é possível despertar dois poderes de mesma cor
                            stack.append(color)

        for i in range(0,4):
            for j in range(0,5):
                color = p[i][j]
                if color in globals.COLORS and color != 'x' and color == p[i+1][j] and color == p[i+2][j]:
                    points = dfs(p,color,i,j)

                    if points:
                        state['score'][turn] += points
                        if color not in stack:
                            stack.append(color)

        if not drop_free_bubblees(p):
            break
    
    if len(stack) != 0:
        state['turn_power'] = turn
        state['power_stack'].append([turn,stack])
        state['current_state'] = globals.STATE_CHOOSE_POWER
    else:
        state['turn'] = (turn+1)%2
        state['current_state'] = globals.STATE_CHECK_WIN

    return state                    

def remove_power(state,power):
    stack = state.get('power_stack')
    stack[-1][1].remove(power)
    if len(stack[-1][1]) == 0:
        stack.pop()
    
def ACCEPT_POWER(state,data):
    if not verify_power(state,data):
        remove_power(state,data)
        stack = state.get('power_stack')

        if len(stack) == 0:
            state['turn_power'] = -1
            state['current_state'] = globals.STATE_SETUP_SKY
        
    else:
        navigate_to_power(state,data)
        remove_power(state,data)

    return state

def navigate_to_power(state,power):
    if power == 'y':
        state['current_state'] = globals.STATE_POWER_YELLOW
    elif power == 'r':
        state['current_state'] = globals.STATE_POWER_RED
    elif power == 'b':
        state['current_state'] = globals.STATE_POWER_BLUE
    elif power == 'g':
        state['current_state'] = globals.STATE_POWER_GREEN
    elif power == 'p':
        state['current_state'] = globals.STATE_POWER_PURPLE

def REJECT_POWER(state,data):
    remove_power(state,data)

    if len(state.get('power_stack')) == 0:
        state['turn_power'] = -1
        state['current_turn'] = globals.STATE_CHECK_WIN
        state['turn'] = (state.get('turn')+1)%2

    return state

def verify_power(state,data):
    turn_power = state.get('power_stack')[-1][0]

    if data == 'y':
        return verify_yellow(state,turn_power)
    if data == 'r':
        return verify_red(state,turn_power)
    if data == 'g':
        return verify_green(state,turn_power)
    if data == 'p':
        return verify_purple(state,turn_power)
    if data == 'b':
        return verify_blue(state,turn_power)
       
def verify_yellow(state,turn_power):
    p = state.get('planet')[turn_power]

    for i in range(0,4):
        for j in range(0,5):
            if p[i][j] in globals.COLORS:
                return True
    return False

def verify_red(state,turn_power):
    p = state.get('planet')[(turn_power+1)%2]

    for i in range(0,3):
        for j in range(0,5):
            if p[i][j] in globals.COLORS and p[i+1][j] in globals.COLORS:
                return True
    
    for i in range(0,4):
        for j in range(0,4):
            if p[i][j] in globals.COLORS and p[i][j+1] in globals.COLORS:
                return True

    return False

def verify_blue(state,turn_power):
    pass

def verify_green(state,turn_power):
    return verify_red(state,(turn_power+1)%2)

def verify_purple(state,turn_power):
    pass

def POWER_YELLOW(state,data):
    turn_power = state.get('turn_power')
    p = state.get('planet')[turn_power]

    state['score'][turn_power]+=1
    p[data[0]][data[1]] = ' '
    drop_free_bubblees(p)

    if len(state.get('power_stack')) == 0:
        state['turn_power'] = -1
    
    state['current_state'] = globals.STATE_CHECK_WIN
    return state

def POWER_RED(state,data):
    p = state.get('planet')[(state.get('turn_power')+1)%2]

    c1,c2 = data
    aux = p[c1[0]][c1[1]]
    p[c1[0]][c1[1]] = p[c2[0]][c2[1]]
    p[c2[0]][c2[1]] = aux

    state['current_state'] = globals.STATE_CHECK_MATCHES
    return state

def POWER_GREEN(state,data):
    p = state.get('planet')[state.get('turn_power')]

    c1,c2 = data
    aux = p[c1[0]][c1[1]]
    p[c1[0]][c1[1]] = p[c2[0]][c2[1]]
    p[c2[0]][c2[1]] = aux

    state['current_state'] = globals.STATE_CHECK_MATCHES
    return state