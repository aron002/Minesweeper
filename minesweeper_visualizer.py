# TODO: 
# Add flag and bomb assets
# Add winner and loser screen/pop up
# Add timer
# Add restart button
# Add flag count


import pygame
from minesweeper import *


def draw_lines():
    line_width = 2
    for i in range(GAME_WIDTH):
        i = WIDTH//GAME_WIDTH * i
        pygame.draw.line(display, (0, 0, 0), (i, 0), (i, HEIGHT), line_width)
    for j in range(GAME_HEIGHT):
        j = HEIGHT//GAME_HEIGHT * j
        pygame.draw.line(display, (0, 0, 0), (0, j), (WIDTH, j), line_width)


def draw_board(minesweeper, board_type, pos):
    # board_type 0 - revealed 1 - full
    row, col = pos
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH):
            char = [minesweeper.revealed_board[i][j], minesweeper.board[i][j]][board_type]
            box_rect = pygame.Rect(WIDTH//GAME_WIDTH*j, HEIGHT//GAME_HEIGHT*i, WIDTH//GAME_WIDTH*(j+1), HEIGHT//GAME_HEIGHT*(i+1))
            if char != ' ':
                if board_type == 1 and row == i and col == j:
                    pygame.draw.rect(display, (155, 0, 0), box_rect)
                else:
                    pygame.draw.rect(display, (255, 255, 255), box_rect)
                if char == '0':
                    char = ' '
                text = font.render(char, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = ((WIDTH//GAME_WIDTH*j + WIDTH//GAME_WIDTH*(j+1))//2, (HEIGHT//GAME_HEIGHT*i + HEIGHT//GAME_HEIGHT*(i+1))//2)
                display.blit(text, text_rect)
            else:
                pygame.draw.rect(display, (200, 200, 200), box_rect)


def draw(minesweeper, board_type, pos):
    display.fill((200, 200, 200))
    draw_board(minesweeper, board_type, pos)
    draw_lines()
    pygame.display.update()


def find_box(pos):
    x, y = pos
    return y//(HEIGHT//GAME_HEIGHT), x//(WIDTH//GAME_WIDTH)


def run():
    stop = False
    minesweeper = Minesweeper(GAME_WIDTH, GAME_HEIGHT, BOMBS)
    board_type = 0
    flags = []
    completed = False
    lose_pos = (0, 0)
    # minesweeper.print_board()
    while not stop:
        pos = pygame.mouse.get_pos()
        row, col = find_box(pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not completed:
                if not minesweeper.click((row, col)):
                    lose_pos = (row, col)
                    board_type = 1
                    print('YOU LOSE')
                    completed = True
                # minesweeper.print_revealed_board()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and not completed:
                minesweeper.place_flag((row, col))
            if minesweeper.check_win() and not completed:
                print('YOU WIN!')
                completed = True
        draw(minesweeper, board_type, lose_pos)
    pygame.quit()


if __name__ == '__main__':
    DIFFICULTIES = {'Easy': {'Width': 10, 'Height': 8, 'Bombs': 10, 'textSize': 48}, 'Medium': {'Width': 18, 'Height': 14, 'Bombs': 40, 'textSize': 36}, 'Hard': {'Width': 24, 'Height': 20, 'Bombs': 99, 'textSize': 24}, 'Test': {'Width': 2, 'Height': 2, 'Bombs': 1, 'textSize': 96}}
    DIFFICULTY = 'Easy'

    GAME_WIDTH = DIFFICULTIES[DIFFICULTY]['Width']
    GAME_HEIGHT = DIFFICULTIES[DIFFICULTY]['Height']
    BOMBS = DIFFICULTIES[DIFFICULTY]['Bombs']
    TEXTSIZE = DIFFICULTIES[DIFFICULTY]['textSize']

    WIDTH, HEIGHT = 800, 800 
    RESOLUTION = (WIDTH, HEIGHT)

    pygame.init()
    display = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('Minesweeper')
    font = pygame.font.Font('freesansbold.ttf', TEXTSIZE)
    run()