# --- Variáveis de Estado ---
STATE_SETUP_SKY = 0
STATE_SWAP_BUBBLEES = 1
STATE_DROP_BUBBLEES = 2
STATE_CHECK_MATCHES = 3
STATE_CHECK_WIN = 5
STATE_ENDGAME = 6
STATE_CHOOSE_POWER = 7
STATE_POWER_RED = 8
STATE_POWER_BLUE = 9
STATE_POWER_YELLOW = 10
STATE_POWER_PURPLE = 11
STATE_POWER_GREEN = 12

# --- Dados de Conversão Para JSON ---
ASCII = {
        'r':'red',
        'b':'blue',
        'y':'yellow',
        'p':'purple',
        'g':'green',
        'x':'black',
}

# --- Outras Variáveis ---
COLORS = list(ASCII.keys())