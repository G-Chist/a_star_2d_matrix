import math


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
    start_point = find_element(matrix, 2)
    start_row = start_point[0]
    start_column = start_point[1]
    end_point = find_element(matrix, 3)
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

    last_points = [[0, 0] for point in points]
    path_costs = [float('inf') for point in points]

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
        if point1[0] == point2[0]:
            if point1[1] == point2[1]:
                return 0
        if point1[0] == point2[0] or point1[1] == point2[1]:
            return 1
        else:
            return 1.41

    def neighbours_available(point):
        neighbours = []
        for direction in directions:
            d_row = point[0] + direction[0]
            d_col = point[1] + direction[1]
            if in_matrix(matrix, d_row, d_col):
                if matrix[d_row][d_col] != 1:
                    neighbours.append([d_row, d_col])
        return neighbours

    def search():
        global chosen_point

        #Stop if end_point is in closed_stack
        if end_point in closed_stack:
            return 0

        if chosen_point not in closed_stack:
            closed_stack.append(chosen_point)

        neighbours = neighbours_available(chosen_point)

        #Put neighbours in open_stack
        for n in neighbours:
            if n not in closed_stack:
                if n not in open_stack:
                    open_stack.append(n)

        #Update last point and path cost
        for p in points:
            if p in neighbours and p not in closed_stack:
                p_index = points.index(p)
                cost = step_cost(chosen_point, p) + h_cost(p)
                if cost < path_costs[p_index]:
                    path_costs[p_index] = cost
                    last_points[p_index] = chosen_point

        #Select next point to explore (lowest cost)
        min_cost_available = float('inf')
        for p in open_stack:
            if p not in closed_stack:
                p_index = points.index(p)
                if path_costs[p_index] < min_cost_available:
                    min_cost_available = path_costs[p_index]
        for p in open_stack:
            if p not in closed_stack:
                p_index = points.index(p)
                if path_costs[p_index] == min_cost_available:
                    chosen_point = p

        """
        print(f"Open stack:        {open_stack}")
        print(f"Closed stack:      {closed_stack}")
        print(f"Points array:      {points}")
        print(f"Last points array: {last_points}")
        print(f"Path costs:        {path_costs}")
        print(f"Chosen point:      {chosen_point}")
        print()
        """

    while end_point not in closed_stack:
        search()

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

    return path


field = [
[0, 0, 0, 0, 0],
[0, 2, 0, 1, 1],
[0, 0, 1, 1, 0],
[0, 1, 0, 0, 3]]

field_path = search_path(field)
print(f"Path: {field_path}")
