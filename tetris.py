import pygame
import random
import streamlit as st

# Streamlit title
st.title("Tetris Game")

# 초기화
pygame.init()

# 화면 크기 설정
width = 300
height = 600
screen = pygame.display.set_mode((width, height))

# 게임 속도 조절
clock = pygame.time.Clock()

# 색상 설정
colors = [
    (0, 0, 0),       # 배경
    (255, 0, 0),     # 빨강
    (0, 255, 0),     # 초록
    (0, 0, 255),     # 파랑
    (255, 255, 0),   # 노랑
    (255, 165, 0),   # 주황
    (128, 0, 128),   # 보라
    (0, 255, 255),   # 청록
]

# 블록 구조 정의
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * 30, y * 30, 30, 30), 0)
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 5)

def clear_rows(grid, locked):
    inc = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            inc += 1
            del locked[(x, y) for x in range(len(row))]
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, row = key
                if row < y:
                    locked[(x, row + inc)] = locked.pop(key)
    return inc

def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    draw_grid(surface, grid)
    pygame.display.update()

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def valid_space(shape, grid):
    pass

def check_lost(positions):
    pass

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_shape()
    next_piece = get_shape()
    change_piece = False
    run = True
    while run:
        grid = create_grid(locked_positions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(screen, grid)
        clock.tick(10)

main()
pygame.quit()