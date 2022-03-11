from pagecollect import *

bfs_visited = [ [3, 1],  [4, 1], [3, 2], [5, 1], [4, 2],  [6, 1],[5, 2], [4, 3], [7, 1],[6, 2],[7, 2], [6, 3], [7, 3], [7, 4], [7, 5],[7, 6],
               [7, 7],
               [6, 7],
               [5, 7],
               [4, 7],
               [4, 6],
               [3, 7],
               [4, 5],
               [3, 6],
               [2, 7],
               [5, 5],
               [3, 5], ]

# astar_visited =[
# [3, 1] ,
# [3, 2] ,
# [4, 1] ,
# [4, 2] ,
# [4, 3] ,
# [5, 1] ,
# [5, 2] ,
# [6, 1] ,
# [6, 2] ,
# [6, 3] ,
# [7, 1] ,
# [7, 2] ,
# [7, 3] ,
# [7, 4] ,
# [7, 5] ,
# [7, 6] ,
# [7, 7] ,
# [6, 7] ,
# [5, 7] ,
# [4, 7] ,
# [4, 6] ,
# [4, 5] ,
# [3, 7] ,
# [3, 6] ,
# [3, 5] ,
# ]
astar_visited = [[2, 1] ,
[3, 1] ,
[3, 2] ,
[4, 2] ,
[4, 3] ,
[4, 1] ,
[5, 2] ,
[5, 1] ,
[6, 2] ,
[6, 3] ,
[6, 1] ,
[7, 2] ,
[7, 1] ,
[7, 3] ,
[7, 4] ,
[7, 5] ,
[7, 6] ,
[7, 7] ,
[6, 7] ,
[5, 7] ,
[4, 7] ,
[4, 6] ,
[4, 5] ,
[3, 5] ,
[3, 6] ,
[2, 5] ,
[2, 4] ,
[3, 7] ,
[5, 5] ,
[2, 6] ,
[5, 4] ,
[2, 7] ,
[1, 5] ,
[1, 6] ,
[1, 4] ,
[1, 7]]
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./pagecollect.py <path_to_instance_file>")

    problem = PageCollect.load(sys.argv[1])
    # print(problem.initial.grid)
    # print(problem.goal)


    # print_info(problem)

    # IF YOU ARE USING BFS PUT FALSE this will allow optimisations for bfs
    copy_grid = [x[:] for x in problem.initial.grid]
    print(copy_grid)
    index = 1
    visited= astar_visited
    print(type(visited[0]))
    for i in range(len(visited)):
        copy_grid[int(visited[i][0])][ visited[i][1]] = index

        first_value = visited[i][1] - 0.5
        second_value = 7-visited[i][0]+0.5
        print("          \\node at ("+ str(first_value)+","+str(second_value)+") {"+str(index)+"};")
        index += 1

    for i in copy_grid:
        print(i)
