from sys import exit
from os.path import join
import pygame


CELL_SIZE = 50
ROWS = 13
COLS = 25
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# colors
LIGHT_GREEN = '#AAD751'
DARK_GREEN = '#A2D149'

#starting position
START_LENGTH = 3
START_ROW= ROWS // 2
START_COL= START_LENGTH+ 2


#SHADOWS
SHADOW_SIZE=pygame.Vector2(4,4)
SHADOW_OPACITY= 50
