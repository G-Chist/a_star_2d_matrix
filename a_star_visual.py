import pygame
import sys
import math
import time


def find_element(arr, target):
    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if arr[row][col] == target:
                return [row, col]
    return None  # Return None if the element is not found


def sum_arrays(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def in_matrix(matrix, row, col):
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0
    return 0 <= row < num_rows and 0 <= col < num_cols


def distance(x1, x2, y1, y2):
    return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)


def search_path(matrix):
    start_point = find_element(matrix, RED)
    start_row = start_point[0]
    start_column = start_point[1]
    end_point = find_element(matrix, BLUE)
    end_row = end_point[0]
    end_column = end_point[1]

    directions = [(-1, -1), (-1, 0), (0, -1), (1, 1), (0, 1), (1, 0), (1, -1), (-1, 1)]
    open_stack = []
    closed_stack = []
    global chosen_point
    chosen_point = start_point

    #Table (points array, last points array, path costs)
    points = []
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            points.append([row, col])

    #One index in last_points, path_costs and points corresponds to the same point
    last_points = [[0, 0] for point in points]
    path_costs = [float('inf') if point != start_point else 0 for point in points]

    """
    print(f"Points array:      {points}")
    print(f"Last points array: {last_points}")
    print(f"Path costs:        {path_costs}")
    print()
    """

    def h_cost(point):
        end_cost = distance(point[0], end_row, point[1], end_column)
        return end_cost

    def step_cost(point1, point2):
        return distance(point1[0], point2[0], point1[1], point2[1])

    def neighbours_available(point):
        neighbours = []
        for direction in directions:
            d_row = point[0] + direction[0]
            d_col = point[1] + direction[1]
            if in_matrix(matrix, d_row, d_col):
                if matrix[d_row][d_col] != BLACK:
                    if abs(direction[0]) == abs(direction[1]): #Cannot pass between two diagonal obstacles
                        if matrix[point[0]][d_col] != BLACK and matrix[d_row][point[1]] != BLACK:
                            neighbours.append([d_row, d_col])
                    else:
                        neighbours.append([d_row, d_col])
        return neighbours

    def search():
        global chosen_point

        #Index of chosen_point in points
        chosen_index = points.index(chosen_point)

        #Check available neighbours
        neighbours = neighbours_available(chosen_point)

        #Update neighbours' costs and last points
        for neighbour in neighbours:
            if neighbour not in open_stack and neighbour not in closed_stack:
                open_stack.append(neighbour)
            if neighbour not in closed_stack:
                n_index = points.index(neighbour) #Index of neighbour in points
                n_last_index = n_index #Index of neighbour's last point in last_points
                cost = step_cost(chosen_point, neighbour) + path_costs[chosen_index] #Cost to get to neighbour

                #Update cost and last point if a better path is found
                if cost < path_costs[n_index]:
                    path_costs[n_index] = cost
                    last_points[n_last_index] = chosen_point

        #Put chosen point in closed stack
        closed_stack.append(chosen_point)

        #Update open stack
        if chosen_point in open_stack:
            open_stack.remove(chosen_point)

        #Choose new point
        full_costs = sum_arrays(path_costs, [h_cost(point) for point in points])
        min_cost = float('inf')
        for point in open_stack:
            p_index = points.index(point) #Index of point in points
            if full_costs[p_index] < min_cost:
                min_cost = full_costs[p_index]

        for point in open_stack:
            p_index = points.index(point)  #Index of point in points
            if full_costs[p_index] == min_cost:
                chosen_point = points[p_index]

        """
        print(f"Open stack:        {open_stack}")
        print(f"Closed stack:      {closed_stack}")
        print(f"Points array:      {points}")
        print(f"Last points array: {last_points}")
        print(f"Path costs:        {path_costs}")
        print(f"Chosen point:      {chosen_point}")
        print()
        """

        for point in open_stack:
            xcor = point[0]
            ycor = point[1]
            button_colors[xcor][ycor] = LIGHT_GREEN

        for point in closed_stack:
            xcor = point[0]
            ycor = point[1]
            button_colors[xcor][ycor] = DARK_GREEN

    while end_point not in closed_stack:
        search()
        screen.fill(GRAY)
        draw_buttons()
        pygame.display.flip()
        #time.sleep(0.005)

    path = []
    last_point = end_point

    while start_point not in path:
        for p in points:
            if p == last_point:
                path.append(last_point)
                p_index = points.index(p)
                last_point = last_points[p_index]
            if last_point == start_point:
                path.append(start_point)
                break

    path.reverse()

    for point in path:
        xcor = point[0]
        ycor = point[1]
        button_colors[xcor][ycor] = PURPLE

    button_colors[start_row][start_column] = RED
    button_colors[end_row][end_column] = BLUE

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 60
BUTTON_SIZE = WIDTH // GRID_SIZE

# Colors
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
LIGHT_GREEN = (155, 251, 167)
DARK_GREEN = (14, 115, 26)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* visual pathfinding showcase")

# Create a 2D array to store button colors
button_colors = [[GRAY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


# Function to draw the grid of buttons
def draw_buttons():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, button_colors[x][y], (x * BUTTON_SIZE, y * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * BUTTON_SIZE, y * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 1)


# Game loop
running = True
mouse_down_l = False
mouse_down_r = False

print("Controls:")
print("LMB - place obstacle")
print("RMB - clear tile")
print("S - place starting point")
print("E - place end point")
print("R - run the search algorithm")
print("C - clear grid")

while running:
    for event in pygame.event.get():

        # Get the state of all keys
        keys = pygame.key.get_pressed()

        # Get the current mouse position
        x, y = pygame.mouse.get_pos()

        if keys[pygame.K_c]:  # Clear board on C press
            button_colors = [[GRAY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        if event.type == pygame.KEYDOWN: # Run search on R release
            if event.key == pygame.K_r:
                key_r_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r and key_r_pressed:
                search_path(button_colors)
                key_r_pressed = False

        if keys[pygame.K_s]: # Start point on S press
            # Erase previous start point
            for i in range(len(button_colors)):
                for j in range(len(button_colors[0])):
                    if button_colors[i][j] == RED:
                        button_colors[i][j] = GRAY
            grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
            # -> red
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                button_colors[grid_x][grid_y] = RED

        if keys[pygame.K_e]: # End point on E press
            # Erase previous end point
            for i in range(len(button_colors)):
                for j in range(len(button_colors[0])):
                    if button_colors[i][j] == BLUE:
                        button_colors[i][j] = GRAY
            grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
            # -> blue
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                button_colors[grid_x][grid_y] = BLUE

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:  # Left mouse button
                mouse_down_l = True
                grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
                # -> black
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    button_colors[grid_x][grid_y] = BLACK

            if event.button == 3:  # Right mouse button
                mouse_down_r = True
                grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
                # -> gray
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    button_colors[grid_x][grid_y] = GRAY

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down_l = False
            if event.button == 3:
                mouse_down_r = False

        elif event.type == pygame.MOUSEMOTION and mouse_down_l: # Holding LMB
            grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
            # -> black
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                button_colors[grid_x][grid_y] = BLACK

        elif event.type == pygame.MOUSEMOTION and mouse_down_r: # Holding RMB
            grid_x, grid_y = x // BUTTON_SIZE, y // BUTTON_SIZE
            # -> gray
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                button_colors[grid_x][grid_y] = GRAY

    # Clear the screen
    screen.fill(GRAY)

    # Draw the buttons and grid lines
    draw_buttons()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
