# coding: utf-8

STANDARD_INGAME_CONST = {
    'SOUNDS_ON': True,
    'START_PLAYER_MONEY': 1000,
    'PLAYER_MONEY_PER_TURN_TO': 10,
    'BLOCK_HEALTH': 75,
    'CAMERA_SPEED': 15,
    'FULLSCREEN_ON': True,
    'TANKS_SPEED': 5,
    'RESOLUTION': (1280, 720),
    'MUSIC_VOLUME': 1000,
    'MINE_MONEY_PER_TURN_TO': 20,
    'SKILLS_LINE_SPEED': 20,
    'MENU_ANIM_SPEED': 1000,
    'OBJ_WIDTH': 50,
    'SOUNDS_VOLUME': 1000,
    'FPS_LIMIT': 60,
    'MINE_MONEY_PER_TURN_FROM': 0,
    'PLAYER_MONEY_PER_TURN_FROM': 0,
    'START_MINE_MONEY': 100,
    'BASE_HEALTH': 1200,
    'BULLETS_SPEED': 15,
    'INFORMATION_LINE_SPEED': 4,
    'OBJ_HEIGHT': 50,
    'MUSIC_ON': True,
    'MINI_MENU_SPEED': 5
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270

KEYS_DICT = {96: "`", 49: "1", 50: "2",
             51: "3", 52: "4", 53: "5",
             54: "6", 55: "7", 56: "8",
             57: "9", 48: "0", 45: "-",
             61: "=", 113: "q", 119: "w",
             101: "e", 114: "r", 116: "t",
             121: "y", 117: "u", 105: "i",
             111: "o", 112: "p", 91: "[",
             93: "]", 92: "\\", 97: "a",
             115: "s", 100: "d", 102: "f",
             103: "g", 104: "h", 106: "j",
             107: "k", 108: "l", 59: ";",
             39: "'", 122: "z", 120: "x",
             99: "c", 118: "v", 98: "b",
             110: "n", 109: "m", 44: ",",
             46: ".", 47: "/", 9: 'Tab',
             301: 'CapsLock', 304: 'LShift',
             306: 'LCtrl', 311: 'Windows',
             308: 'LAlt', 305: 'RCtrl',
             307: 'RAlt', 303: 'RShift',
             32: 'Spacebar', 282: 'F1',
             283: 'F2', 284: 'F3',
             285: 'F4', 286: 'F5',
             287: 'F6', 288: 'F7',
             289: 'F8', 290: 'F9',
             291: 'F10', 292: 'F11',
             293: 'F12', 273: 'Up',
             274: 'Down', 275: 'Right',
             276: 'Left', 278: 'Home',
             279: 'End', 280: 'PgUp',
             281: 'PgDn', 27: 'Escape',
             13: 'Enter'
}

STANDARD_CONTROLS = {1: {'shoot': 113, 'base': 101, 'right': 100, 'turn_end': 13, 'down': 115, 'up': 119, 'left': 97},
                     2: {'shoot': 113, 'base': 101, 'right': 100, 'turn_end': 13, 'down': 115, 'up': 119, 'left': 97}}
