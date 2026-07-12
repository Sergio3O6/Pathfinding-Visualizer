'''
To run program. Start the program. Click your first starting point and choose your second point.
Once points are selected press space and watch.
'''


import pygame
import collections


WIDTH, HEIGHT = 800, 800 #Window size
ROWS = 40
GRID_SIZE = WIDTH // ROWS 
WHITE, BLACK, RED, GREEN, BLUE, GREY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200) #Sets color with RGB

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = WHITE
        self.neighbors = []
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == BLUE

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_path(self):
        self.color = BLUE

    def reset(self):
        self.color = WHITE

    def draw(self, win ): #Creates window
        pygame.draw.rect(win, self.color, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(win, GREY, (self.col * GRID_SIZE, self.row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def make_grid(): #Creates grid
    return [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)] 

def draw(win, grid): #Draws on the grid to show progression of algorithm
    for row in grid:
        for node in row: node.draw(win)
    pygame.display.update()

def bfs(win, grid, start, end):
    queue = collections.deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == end:
            #Reconstruct path
            while current:
                current.color = BLUE
                current = parent[current]
                draw(win, grid)
            return True
            
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            r, c = current.row + dr, current.col + dc
            if 0 <= r < ROWS and 0 <= c < ROWS and grid[r][c].color != BLACK and grid[r][c] not in visited:
                visited.add(grid[r][c])
                parent[grid[r][c]] = current
                queue.append(grid[r][c])
                grid[r][c].color = GREEN #Visualize exploration
                draw(win, grid)
    return False

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    grid = make_grid()
    start, end = None, None
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Seperates first and second clicks
                pos = pygame.mouse.get_pos()
                r, c = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                node = grid[r][c]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    bfs(win, grid, start, end)
                if event.key == pygame.K_r: #Pressing r resets the board
                    grid = make_grid()
                    start, end = None, None

            if start and end and pygame.mouse.get_pressed()[0]: #For drawing walls
                pos = pygame.mouse.get_pos()
                r, c = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                node = grid[r][c]
                if node != start and node != end:
                    node.make_barrier()
    pygame.quit()

if __name__ == "__main__":
    main()