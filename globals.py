# --- Variáveis de Estado ---
STATE_SETUP_SKY = 0
STATE_SWAP_BUBBLEES = 1
STATE_DROP_BUBBLEES = 2
STATE_CHECK_MATCHES = 3
STATE_USE_POWER = 4
STATE_CHECK_WIN = 5
STATE_ENDGAME = 6
STATE_CHOOSE_POWER = 7
STATE_VERIFY_POWER = 8

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