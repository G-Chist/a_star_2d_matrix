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
                if matrix[d_row][d_col] != 1:
                    if abs(direction[0]) == abs(direction[1]): #Cannot pass between two diagonal obstacles
                        if matrix[point[0]][d_col] != 1 and matrix[d_row][point[1]] != 1:
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
            p_index = points.index(point)  #Index of point in points
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

    while end_point not in closed_stack:
        search()
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

    return path

if __name__ == "__main__":

    field = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0],
    [2, 1, 0, 0, 3]]

    field_path = search_path(field)
    print(f"Path: {field_path}")
