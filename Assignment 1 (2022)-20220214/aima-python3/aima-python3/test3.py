class fuckyou:
    def move_row(self, list_grid, axe_number, n_move):
        line = list_grid[axe_number]
        n_column = len(list_grid[0])
        new_line = line[slice(n_column - n_move, n_column)] + line[slice(0, n_column - n_move)]
        return new_line

if __name__ == "__main__":
    def move_row( list_grid, axe_number, n_move):
        line = list_grid[axe_number]
        n_column = len(list_grid[0])
        new_line = line[slice(n_column - n_move, n_column)] + line[slice(0, n_column - n_move)]
        return new_line
    test = [('1', '1', '3', '3'), ('.', '.', '.', '.'), ('.', '.', '.', '.'), ('.', '.', '.', '.')]
    print(move_row(test,0,1))

