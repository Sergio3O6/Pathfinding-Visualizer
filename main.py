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
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
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

    def update_neighbors(self, grid):
        self.neighbors = []
        r, c = self.row, self.col
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]: #Checks all 4 directions
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < ROWS and not grid[nr][nc].is_barrier():
                self.neighbors.append(grid[nr][nc]) #Only adds if it's on the board and not a wall


class Pathfinding:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grid = self.make_grid()
        self.start: Node | None = None
        self.end: Node | None = None
        self.running = True
        self.clock = pygame.time.Clock()

    def make_grid(self): #Creates grid
        return [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)] 

    def draw(self): #Draws on the grid to show progression of algorithm
        for row in self.grid:
            for node in row:
                node.draw(self.win)
        pygame.display.update()

    def reset(self):
        self.grid = self.make_grid()
        self.start = None
        self.end = None

    def bfs(self):
        if self.start is None or self.end is None:
            return False
        queue = collections.deque([self.start])
        visited = {self.start}
        parent: dict[Node, Node | None] = {self.start: None}
        
        while queue:
            current = queue.popleft()
            if current == self.end:
                #Reconstruct path
                while current:
                    current.make_path()
                    current = parent.get(current)
                    if current:
                        self.draw()
                self.start.make_start()
                return True
                
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

                    if neighbor != self.end:
                        neighbor.make_open()
                    self.draw()
        return False

    def refresh_all_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def run_algorithm(self):
        self.refresh_all_neighbors()
        self.bfs()

    def handle_event(self, event):
        if event.type == pygame.QUIT: 
            self.running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Seperates first and second clicks
            pos = pygame.mouse.get_pos()
            r, c = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
            node = self.grid[r][c]
            if not self.start and node != self.end:
                self.start = node
                self.start.make_start()
            elif not self.end and node != self.start:
                self.end = node
                self.end.make_end()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.start and self.end:
                self.run_algorithm()
            if event.key == pygame.K_r: #Pressing r resets the board
               self.reset()

        if self.start and self.end and pygame.mouse.get_pressed()[0]: #For drawing walls
            pos = pygame.mouse.get_pos()
            r, c = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
            node = self.grid[r][c]
            if node != self.start and node != self.end:
                node.make_barrier()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                self.handle_event(event)
        pygame.quit()

if __name__ == "__main__":
    app = Pathfinding()
    app.run()