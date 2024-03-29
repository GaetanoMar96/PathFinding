import heapq
import pygame

class Astar:

    def reconstruct_path(self, came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

    def heuristic(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def algorithm(self, draw, grid, start, end):
        count = 0
        q = []
        heapq.heappush(q, (0, count, start))
        came_from = {}
        g_score = {spot: float('inf') for row in grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float('inf') for row in grid for spot in row}
        f_score[start] = self.heuristic(start.get_pos(), end.get_pos())

        visited = {start}

        while q:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            _, count, current = heapq.heappop(q)
            visited.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end, draw)
                end.make_end()
                return

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score

                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor.get_pos(), end.get_pos())
                    if neighbor not in visited:
                        count += 1
                        heapq.heappush(q, (f_score[neighbor], count, neighbor))
                        visited.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()
    
  
