'''
To run program. Start the program. Click your first starting point and choose your second point.
Once points are selected press space and watch.
'''

import heapq
import pygame
import collections
import time


WIDTH, HEIGHT = 800, 800 #Window size
STATS_HEIGHT = 60
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
        self.win = pygame.display.set_mode((WIDTH, HEIGHT + STATS_HEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 18)
        self.stats: dict = {}
        self.grid = self.make_grid()
        self.start: Node | None = None
        self.end: Node | None = None
        self.running = True
        self.clock = pygame.time.Clock()
        self.algorithm = 'bfs'

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
                path_length = 0
                #Reconstruct path
                while current:
                    current.make_path()
                    current = parent.get(current)
                    if current:
                        self.draw()
                self.start.make_start()
                self._last_run_stats = {'nodes_visited': len(visited), 'path_length': path_length}
                return True
                
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

                    if neighbor != self.end:
                        neighbor.make_open()
                    self.draw()
        self._last_run_stats = {'nodes_visited': len(visited), 'path_length': 0}
        return False

    def dijkstra(self):
        if self.start is None or self.end is None:
            return False

        count = 0   
        open_heap = [(0, count, self.start)]
        g_score = {node: float('inf') for row in self.grid for node in row}
        g_score[self.start] = 0
        parent: dict[Node, Node | None] = {self.start: None}
        visited = set()

        while open_heap:
            current_g, _, current = heapq.heappop(open_heap)
            if current in visited:
                continue
            visited.add(current)

            if current == self.end:
                while current:
                    current.make_path()
                    current = parent.get(current)
                    if current:
                        self.draw()
                self.start.make_start()
                return True

            for neighbor in current.neighbors:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    parent[neighbor] = current
                    count += 1
                    heapq.heappush(open_heap, (tentative_g, count, neighbor))
                    if neighbor != self.end:
                        neighbor.make_open()
            self.draw()
        return False
    
    def heuristic(self, a: Node, b: Node) -> int:
        # Manhattan distance — admissible here since moves are only up/down/left/right at cost 1
        return abs(a.row - b.row) + abs(a.col - b.col)

    def astar(self):
        if self.start is None or self.end is None:
            return False

        count = 0
        open_heap = [(0, count, self.start)]
        g_score = {node: float('inf') for row in self.grid for node in row}
        g_score[self.start] = 0
        parent: dict[Node, Node | None] = {self.start: None}
        visited = set()

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current in visited:
                continue
            visited.add(current)

            if current == self.end:
                while current:
                    current.make_path()
                    current = parent.get(current)
                    if current:
                        self.draw()
                self.start.make_start()
                return True

            for neighbor in current.neighbors:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    parent[neighbor] = current
                    f_score = tentative_g + self.heuristic(neighbor, self.end)
                    count += 1
                    heapq.heappush(open_heap, (f_score, count, neighbor))
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

        start_time = time.perf_counter()
        if self.algorithm == 'bfs':
            self.bfs()
        elif self.algorithm == 'dijkstra':
            self.dijkstra()
        elif self.algorithm == 'astar':
            self.astar()
        else:
            found = False
        elapsed = time.perf_counter() - start_time
        self.stats = {
            'algorithm': self.algorithm,
            'found': found,
            'time_ms': round(elapsed * 1000, 2),
            **self._last_run_stats,
        }

    def draw_ui(self):
        panel_rect = (0, HEIGHT, WIDTH, STATS_HEIGHT)
        pygame.draw.rect(self.win, WHITE, panel_rect)
        pygame.draw.line(self.win, BLACK, (0, HEIGHT), (WIDTH, HEIGHT), 2)

        if not self.stats:
            text = f"Algorithm: {self.algorithm.upper()}  |  Press SPACE to run, 1/2/3 to switch, R to reset"
        else:
            s = self.stats
            status = "found" if s['found'] else "no path"
            text = (f"{s['algorithm'].upper()}  |  {status}  |  "
                    f"{s['time_ms']}ms  |  visited: {s['nodes_visited']}  |  path: {s['path_length']}")

        rendered = self.font.render(text, True, BLACK)
        self.win.blit(rendered, (10, HEIGHT + 18))

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
            if event.key == pygame.K_1:
                self.algorithm = 'bfs'
            if event.key == pygame.K_2:
                self.algorithm = 'dijkstra'
            if event.key == pygame.K_3:
                self.algorithm = 'astar'
            if event.key == pygame.K_r:
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
            self.draw_ui()
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_event(event)
        pygame.quit()

if __name__ == "__main__":
    app = Pathfinding()
    app.run()