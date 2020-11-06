import pygame, sys

ROW_SIZE, COL_SIZE = (50,50) #size of the grid
pygame.init()
win = pygame.display.set_mode((ROW_SIZE * 10-5, COL_SIZE * 10-5))
pygame.display.set_caption("game of life")

grid = [[0 for _ in range(ROW_SIZE)] for _ in range(COL_SIZE)]

def draw(grid): #white == alive, black == dead
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                pygame.draw.rect(win, (0, 0, 0), (j * 10, i * 10, 10, 10))
            else:
                pygame.draw.rect(win, (255, 255, 255), (j * 10, i * 10, 10, 10))

def check_neigh(row, col, grid):
    totalNeigh = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            else:
                totalNeigh += grid[(row + j) % len(grid)][(col + i) % len(grid[0])]
    return totalNeigh

def life(old_grid): #creates the new generation
    new_grid = [[0 for _ in range(ROW_SIZE)] for _ in range(COL_SIZE)]

    for i in range(len(old_grid)):
        for j in range(len(old_grid[0])):
            neighnum = check_neigh(i, j, old_grid)

            if old_grid[i][j] == 0:
                if neighnum == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0

            if old_grid[i][j] == 1:
                if neighnum < 2 or neighnum > 3:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = 1
    return new_grid

generation_life = 0
clock = pygame.time.Clock()
pause_loop = False

while  True:
    dt = clock.tick()
    generation_life += dt

    if pause_loop == True:
        if generation_life > 100: #lifespan of each generation

            grid = life(grid)
            draw(grid)
            generation_life = 0

    for event in pygame.event.get():

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = round(mpos[0], -1); mpos[1] = round(mpos[1], -1)

        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(win, (255, 255, 255), (mpos[0], mpos[1], 10, 10))
            grid[mpos[1]//10][mpos[0]//10] = 1

        if pygame.mouse.get_pressed()[2]:
            pygame.draw.rect(win, (0, 0, 0), (mpos[0], mpos[1], 10, 10))
            grid[mpos[1] // 10][mpos[0] // 10] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause_loop = not pause_loop

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

