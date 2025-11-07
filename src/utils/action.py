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
    
    state['current_state'] = globals.STATE_SETUP_SKY
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
    if state.get('turn_power') == -1:
        turn = state.get('turn')
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

    if len(stack[-1][1]):
        stack.pop()


def ACCEPT_POWER(state,data):
    if not verify_power(state,data):
        remove_power(state,data)
        stack = state.get('power_stack')

    else:
        state['current_state'] = globals.STATE_POWER_YELLOW
        remove_power(state,data)

    return state

def REJECT_POWER(state,data):
    pass

def verify_power(state,data):
    turn_power = state.get('power_stack')[-1][0]

    if data == 'y':
        return verify_yellow(state,turn_power)
    
    
def verify_yellow(state,turn_power):
    p = state.get('planet')[turn_power]

    for i in range(0,4):
        for j in range(0,5):
            if p[i][j] in globals.COLORS:
                return True
    return False