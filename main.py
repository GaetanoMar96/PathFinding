import pygame
from algorithm.node import Node 
from util.colors import Colors
from algorithm.astar import Astar

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


def make_grid(rows, width):
	"""Create a 2D grid of Node objects."""
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([Node(i, j, gap, rows) for j in range(rows)])
	return grid


def draw_grid(win, rows, width):
	"""Draw grid lines on the window."""
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, Colors.GREY.value, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, Colors.GREY.value, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	"""Draw the entire window including nodes and grid lines."""
	win.fill(Colors.WHITE.value)
	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	"""Convert mouse position to grid coordinates."""
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap
	return row, col


def main(win, width):
	"""Main loop for the A* pathfinding visualization."""
	ROWS = 50
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	astar = Astar()

	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					astar.algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

if __name__ == "__main__":
	main(WIN, WIDTH)