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
            
            if pygame.mouse.get_pressed()[0]: # Left Click
                pos = pygame.mouse.get_pos()
                r, c = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                if not start: start = grid[r][c]; start.color = RED
                elif not end: end = grid[r][c]; end.color = RED
                else: grid[r][c].color = BLACK
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    bfs(win, grid, start, end)
    pygame.quit()

if __name__ == "__main__":
    main()