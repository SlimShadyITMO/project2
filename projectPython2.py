import pygame
import sys
import random
from pygame.locals import *

# этот раздел содержит все переменные, которые мы будем использовать в игре-головоломке на Python
w_of_board = 4  # общее количество колонок на доске игры-головоломки на Python
h_of_board = 4  # общее количество строк на доске
block_size = 80
win_width = 640
win_height = 480
FPS = 30
BLANK = None

# это в основном для управления различными цветами компонентов
# мы также использовали переменные для поддержания размера текста в игре-головоломке на Python
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0,  50, 255)
DARKTURQUOISE = (255, 255, 255)
BLUE = (0,  0, 0)
GREEN = (0, 128,   0)
RED = (255, 0, 0)
BGCOLOR = DARKTURQUOISE
TILECOLOR = BLUE
TEXTCOLOR = WHITE
BORDERCOLOR = RED
BASICFONTSIZE = 20
TEXT = GREEN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = GREEN

# это для оставления пространства по обеим сторонам блока
XMARGIN = int((win_width - (block_size * w_of_board + (w_of_board - 1))) / 2)
YMARGIN = int((win_height - (block_size * h_of_board + (h_of_board - 1))) / 2)

# это переменные для обработки клавиш на клавиатуре
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# это основная функция


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((win_width, win_height))
    # мы задали заголовок с помощью функции set_caption в pygame
    pygame.display.set_caption('Слайд-головоломка - Копия задания')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # эти переменные хранят различные опции, которые будут отображаться справа от нашей основной сетки
    # эти ниже только обрабатывают дизайнерскую часть опций
    RESET_SURF, RESET_RECT = makeText(
        'Сброс',    TEXT, BGCOLOR, win_width - 120, win_height - 310)
    NEW_SURF,   NEW_RECT = makeText(
        'Новая игра', TEXT, BGCOLOR, win_width - 120, win_height - 280)
    SOLVE_SURF, SOLVE_RECT = makeText(
        'Решить',    TEXT, BGCOLOR, win_width - 120, win_height - 250)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    # это просто доска, которая такая же, как у решенной доски в игре-головоломке на Python
    # в основном игра перемешает все блоки из решенной игры
    SOLVEDBOARD = start_playing()
    # список, который отслеживает ходы, сделанные из решенной конфигурации
    allMoves = []
    # основной игровой цикл
    while True:
        slideTo = None
        # переменная ниже содержит сообщение для отображения в верхнем левом углу.
        msg = 'Нажмите на блок или используйте стрелки для перемещения блока.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Решено!'

        drawBoard(mainBoard, msg)

        check_exit_req()
        # цикл ниже обрабатывает различные события клавиатуры
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(
                    mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # это проверка, если пользователь нажал на кнопку опции
                    if RESET_RECT.collidepoint(event.pos):
                        # эта строка сработает, если пользователь нажал на кнопку Сброс
                        rst_animation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        # эта строка сработает, если пользователь нажал на кнопку Новая игра
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        # эта строка сработает, если пользователь нажал на кнопку Решить
                        rst_animation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                else:
                    # этот блок else в игре-головоломке на Python просто проверяет, что перемещаемая плитка пуста
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # этот elif блок обрабатывает проверку, если пользователь нажал клавишу для перемещения плитки
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        # этот блок обрабатывает функциональность отображения сообщения для управления
        if slideTo:
            # показать слайд на экране
            sliding_animation(
                mainBoard, slideTo, 'Нажмите на блок или используйте стрелки для перемещения блока.', 8)
            take_turn(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def check_exit_req():
    # получить все события QUIT
    for event in pygame.event.get(QUIT):
        # terminate() убивает все события. завершить, если есть какие-либо события QUIT
        terminate()
    # этот цикл получает все события KEYUP
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            # если пользователь нажимает клавишу ESC, то он завершит сессию, и если событие KEYUP было для клавиши Esc
            terminate()
        # вернем другие объекты событий KEYUP обратно
        pygame.event.post(event)


def start_playing():
    # Вернем структуру доски с блоками в решённом состоянии.
    counter = 1
    board = []
    for x in range(w_of_board):
        column = []
        for y in range(h_of_board):
            column.append(counter)
            counter += w_of_board
        board.append(column)
        counter -= w_of_board * (h_of_board - 1) + w_of_board - 1

    board[w_of_board-1][h_of_board-1] = BLANK
    return board


def getBlankPosition(board):
    # Вернем x и y координаты доски пустого пространства.
    for x in range(w_of_board):
        for y in range(h_of_board):
            if board[x][y] == BLANK:
                return (x, y)


def take_turn(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def ramdom_moves(board, lastMove=None):
    # начать с полного списка всех четырех движений
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # удалить движения из списка, так как они не подходят
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # это выполнит возврат и вернёт случайный ход из оставшихся движений
    return random.choice(validMoves)


def getLeftTopOfTile(block_x, block_y):
    left = XMARGIN + (block_x * block_size) + (block_x - 1)
    top = YMARGIN + (block_y * block_size) + (block_y - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # из координат x и y пикселей, этот цикл ниже получит координаты x и y доски
    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            left, top = getLeftTopOfTile(block_x, block_y)
            tileRect = pygame.Rect(left, top, block_size, block_size)
            if tileRect.collidepoint(x, y):
                return (block_x, block_y)
    return (None, None)


def draw_block(block_x, block_y, number, adjx=0, adjy=0):
    # нарисовать плитку на координатах доски block_x и block_y
    left, top = getLeftTopOfTile(block_x, block_y)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx,
                     top + adjy, block_size, block_size))
    text_renderign = BASICFONT.render(str(number), True, TEXTCOLOR)
    text_in_rect = text_renderign.get_rect()
    text_in_rect.center = left + \
        int(block_size / 2) + adjx, top + int(block_size / 2) + adjy
    DISPLAYSURF.blit(text_renderign, text_in_rect)


def makeText(text, color, bgcolor, top, left):
    # создать Surface и Rect объекты для некоторого текста.
    text_renderign = BASICFONT.render(text, True, color, bgcolor)
    text_in_rect = text_renderign.get_rect()
    text_in_rect.topleft = (top, left)
    return (text_renderign, text_in_rect)

# эта функция нарисует доску, на которой игрок может играть. она содержит код для отображения различных цветов и логики игры


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        text_renderign, text_in_rect = makeText(
            message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(text_renderign, text_in_rect)

    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            if board[block_x][block_y]:
                draw_block(block_x, block_y, board[block_x][block_y])

    left, top = getLeftTopOfTile(0, 0)
    width = w_of_board * block_size
    height = h_of_board * block_size
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5,
                     top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

# эта функция обрабатывает анимацию, которая отображается, когда пользователь начинает новую игру
# пользователь может видеть анимацию скольжения над блоками

def sliding_animation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        move_in_xaxis = blankx
        move_in_yaxis = blanky + 1
    elif direction == DOWN:
        move_in_xaxis = blankx
        move_in_yaxis = blanky - 1
    elif direction == LEFT:
        move_in_xaxis = blankx + 1
        move_in_yaxis = blanky
    elif direction == RIGHT:
        move_in_xaxis = blankx - 1
        move_in_yaxis = blanky

    # подготавливаю поверхность
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # нарисовать пустое пространство над движущимся блоком на поверхности.
    take_left, take_top = getLeftTopOfTile(move_in_xaxis, move_in_yaxis)
    pygame.draw.rect(baseSurf, BGCOLOR, (take_left,
                     take_top, block_size, block_size))

    for i in range(0, block_size, animationSpeed):
        # это для обработки анимации плитки, скользящей по поверхности
        check_exit_req()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, -i)
        if direction == DOWN:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, i)
        if direction == LEFT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], -i, 0)
        if direction == RIGHT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # это для отображения анимации блоков
    sequence = []
    board = start_playing()
    drawBoard(board, '')
    pygame.display.update()
    # мы использовали time.wait() для паузы на 500 миллисекунд для эффекта
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = ramdom_moves(board, lastMove)
        sliding_animation(board, move, 'Генерация новой головоломки...',
                          animationSpeed=int(block_size / 3))
        take_turn(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def rst_animation(board, allMoves):
    # сделать все движения в обратном порядке
    reverse_moves = allMoves[:]
    reverse_moves.reverse()

    for move in reverse_moves:
        if move == UP:
            opp_moves = DOWN
        elif move == DOWN:
            opp_moves = UP
        elif move == RIGHT:
            opp_moves = LEFT
        elif move == LEFT:
            opp_moves = RIGHT
        sliding_animation(board, opp_moves, '',
                          animationSpeed=int(block_size / 2))
        take_turn(board, opp_moves)


# это вызов основной функции
if __name__ == '__main__':
    main()

