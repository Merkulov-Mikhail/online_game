# [1000-2000) -> NETWORK CONSTANTS
# 11 - CONTENT TYPES


# [2000-3000) -> ENTITIES CONSTANTS


# [3000-4000) -> PLAYER CONSTANTS
# 30 - PLAYER MOVING
# 31 - SPECIAL KEY_BINDS


class NETWORK:
    """
    Contains most information about network - address, using port, possible types of package
    """
    ADDRESS = "127.0.0.1"
    PORT = 5051
    TPS = 20
    AUTH_STRING = "AUTH_KEY"

    class CONTENT_TYPES:
        CONNECTIONS = 1100
        CONNECTION_LOST = CONNECTIONS + 1
        AUTH = CONNECTIONS + 2
        UPDATE = CONNECTIONS + 3
        BULLET_SHOT = CONNECTIONS + 4


class GUNS:
    ASSAULT_RIFLE_FIRE_RATE = 2


class ENTITIES:
    """
    Contains IDs of every possible entity in the game
    """
    IDS = 2000
    PLAYER_ID = IDS + 1
    BULLET_ID = IDS + 2
    OBSTACLE_ID = IDS + 3


class BULLET:
    BULLET_SIZE = 10
    BULLET_SPEED = 15

    BASIC_BULLET_DAMAGE = 20


class EVENTS:
    """
    Contains possible events - lights off/on, players inputs e.t.c
    The game checks events in order, in which they are defined here
    If the order of events looks like this
    UP = ..
    DOWN = ..
    LEFT = ..
    RIGHT = ..
    Then game will be firstly checking UP event, then DOWN event, then LEFT event and eventually, RIGHT event
    So if you want the game to firstly check special event before others - you just put it higher
    EXAMPLE:
        Shift modifies movement speed, so I want to check, if the KEY_SHIFT is pressed by player, BEFORE checking movement buttons
        So I put KEY_SHIFT earlier, than UP, DOWN, LEFT, RIGHT
    """
    KEYS = 3100
    KEY_SHIFT = KEYS + 1              # Player is sprinting
    LEFT_MOUSE_DOWN = KEYS + 2        # Player started shooting
    LEFT_MOUSE_UP = KEYS + 3          # Player stopped shooting

    SPECIAL_MODIFICATIONS = 3200
    DIAGONAL_MOVEMENT = SPECIAL_MODIFICATIONS + 1     # If Player moves diagonally

    DIRECTIONS = 3000
    UP = DIRECTIONS + 1               # Player moves upwards
    DOWN = DIRECTIONS + 2             # Player moves downwards
    LEFT = DIRECTIONS + 3             # Player moves to the left
    RIGHT = DIRECTIONS + 4            # Player moves to the right


# TODO: HEALING, DAMAGE, HOTKEYS


# CONSTANTS, THAT ARE NOT USED DURING CLIENT-SERVER COMMUNICATION

class GAME_DEFAULTS:
    DEBUG = True


class PLAYER:
    """
    Contains description of the player
    """
    PLAYER_SIZE = 100
    PLAYER_EYES_RADIUS = PLAYER_SIZE * 0.1125
    MOVEMENT_SPEED = 5
    SPRINT_MULTIPLIER = 1.7
    DIAGONAL_MULTIPLIER = 0.7


class GEOMETRY:
    """
    Possible geometry types
    """
    ELLIPSE = 1
    RECT = 2
    LINE = 3
    TRIANGLE = 4


# COLORS
class COLORS:
    """
    Contains colors
    """
    PLAYER_BORDER = "#282828"
    PLAYER_BODY = "#1c292a"
    PLAYER_EYES = "#000930"
    BULLET = "#808000"
    WHITE = "#FFFFFF"
    DARKNESS_COLOR = "#333333"


# SCREEN
class SCREEN:
    """
    Contains client-side screen config
    """
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 1000
