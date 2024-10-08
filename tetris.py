import pygame
import random
import streamlit as st
import time
import numpy as np
from PIL import Image

# Streamlit title
st.title("Tetris Game")

# 게임 상태 저장
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False
if "game_over" not in st.session_state:
    st.session_state["game_over"] = False

# 초기화
pygame.init()

# 화면 크기 설정
width = 300
height = 600
block_size = 30
screen = pygame.Surface((width, height))  # 화면을 pygame Surface로 설정

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

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]  # 현재 회전 상태의 모양

    # 모양 데이터를 2차원 리스트로 변환
    for i, line in enumerate(format):
        if isinstance(line, list):  # 각 행이 리스트인 경우만 처리
            for j, column in enumerate(line):
                if column == 1:
                    positions.append((piece.x + j, piece.y + i))
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * block_size, y * block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 5)

def clear_rows(grid, locked):
    inc = 0  # 삭제된 행의 수
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        # 행이 꽉 찬 경우
        if (0, 0, 0) not in row:
            inc += 1
            # 행의 모든 블록을 삭제
            for x in range(len(row)):
                try:
                    del locked[(x, y)]  # 잠긴 위치에서 해당 블록을 삭제
                except KeyError:
                    continue
            # 삭제된 행 위의 모든 블록을 아래로 이동
    if inc > 0:
        # 모든 블록을 아래로 이동시키는 로직
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < y + inc:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop((x, y))
    return inc

def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    draw_grid(surface, grid)
    pygame.display.update()

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_shape()
    next_piece = get_shape()
    change_piece = False
    run = True
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27
        fall_time += clock.get_rawtime()
        clock.tick()

        # 블록이 일정 시간마다 아래로 떨어지게 함
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # 사용자 입력 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        # 블록을 그리드에 추가
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = colors[current_piece.color]

        # 블록이 바닥에 닿으면 잠긴 블록으로 설정
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = colors[current_piece.color]
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # 행을 클리어
            clear_rows(grid, locked_positions)

        draw_window(screen, grid)

        # 게임 종료 조건 확인
        if check_lost(locked_positions):
            st.session_state["game_over"] = True
            run = False

        # pygame 화면을 numpy 배열로 변환
        img_array = pygame.surfarray.array3d(screen)
        img_array = np.rot90(img_array)  # 회전 후
        img_array = np.flipud(img_array)  # 좌우 반전

        # numpy 배열을 이미지로 변환
        img = Image.fromarray(img_array)

        # Streamlit을 통해 이미지를 표시
        st.image(img)

    pygame.display.quit()

# Streamlit UI 처리
if not st.session_state["game_started"] and not st.session_state["game_over"]:
    if st.button("게임을 시작합니다"):
        st.session_state["game_started"] = True
        st.session_state["game_over"] = False
        main()

if st.session_state["game_started"]:
    if st.button("종료하기"):
        st.session
