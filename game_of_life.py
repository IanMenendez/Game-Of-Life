import pygame, sys

class Game:
    def __init__(self,cols, rows):
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]


    def draw(self): #white == alive, black == dead
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(win, (0, 0, 0), (j * 10, i * 10, 10, 10))
                else:
                    pygame.draw.rect(win, (255, 255, 255), (j * 10, i * 10, 10, 10))

    def check_neigh(self,row, col):
        totalNeigh = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                else:
                    totalNeigh += self.grid[(row + j) % len(self.grid)][(col + i) % len(self.grid[0])]
        return totalNeigh

    def life(self): #creates the new generation
        new_grid = [[0 for _ in range(COL_SIZE)] for _ in range(ROW_SIZE)]

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                neighnum = self.check_neigh(i, j)

                if self.grid[i][j] == 0:
                    if neighnum == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0

                if self.grid[i][j] == 1:
                    if neighnum < 2 or neighnum > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1

        self.grid = new_grid
        self.draw()

COL_SIZE, ROW_SIZE = (50,50) #size of the grid
pygame.init()
win = pygame.display.set_mode((COL_SIZE * 10, ROW_SIZE * 10))
pygame.display.set_caption("game of life")

game = Game(COL_SIZE, ROW_SIZE)

generation_life = 0
clock = pygame.time.Clock()
pause_loop = False

while  True:
    dt = clock.tick()
    generation_life += dt

    if pause_loop == True:
        if generation_life > 100: #lifespan of each generation
            game.life()
            generation_life = 0

    for event in pygame.event.get():
        mpos = list(pygame.mouse.get_pos())
        mpos[0] = round(mpos[0], -1); mpos[1] = round(mpos[1], -1)

        try:
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(win, (255, 255, 255), (mpos[0], mpos[1], 10, 10))
                game.grid[mpos[1] // 10][mpos[0] // 10] = 1

            if pygame.mouse.get_pressed()[2]:
                pygame.draw.rect(win, (0, 0, 0), (mpos[0], mpos[1], 10, 10))
                game.grid[mpos[1] // 10][mpos[0] // 10] = 0
        except IndexError: #outbound of the window
            pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause_loop = not pause_loop

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

