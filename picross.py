EMPTY = ' '
UNKNOWN = '.'
FILLED = '#'

class Solver:
    def __init__(self, filepath):
        """Load the picross data from a file"""
        self.col_values = []
        self.row_values = []
        with open(filepath) as file:
            self.n_cols, self.n_rows = (
                [int(i) for i in file.readline().split()])
            file.readline()
            for i in range(self.n_cols):
                self.col_values.append(
                    [int(i) for i in file.readline().split()])
            file.readline()
            for i in range(self.n_rows):
                self.row_values.append(
                    [int(i) for i in file.readline().split()])
        self.chart = []
        for n in range(self.n_rows):
            self.chart.append(UNKNOWN * self.n_cols)
        self.row_patterns = []
        for row in self.row_values:
            self.row_patterns.append(
                self.get_possible_arrangements(row, self.n_cols))
        self.col_patterns = []
        for col in self.col_values:
            self.col_patterns.append(
                self.get_possible_arrangements(col, self.n_rows))

    def get_possible_arrangements(self, values, size):
        if sum(values) + len(values) - 1 > size:
            return []
        if len(values) == 0 or values[0] == 0:
            return [EMPTY * size]
        if len(values) == 1 and values[0] == size:
            return [FILLED * size]
        answers = self.get_possible_arrangements(
            values[1:], size - values[0] - 1)
        answers = [FILLED * values[0] + EMPTY + suffix for suffix in answers]
        return answers + [EMPTY + suffix for suffix in self.get_possible_arrangements(values, size - 1)]

    def evaluate_row(self, row):
        patterns = self.row_patterns[row]
        placed = list(self.chart[row])
        patterns, placed = self.evaluate(patterns, placed)
        self.row_patterns[row] = patterns
        self.chart[row] = ''.join(placed)

    def evaluate_col(self, col):
        patterns = self.col_patterns[col]
        placed = self.extract_column(col)
        patterns, placed = self.evaluate(patterns, placed)
        self.col_patterns[col] = patterns
        self.return_column(col, placed)

    def evaluate(self, patterns, placed):
        # eliminate patterns that contradict cells that
        # are already on the board.
        for pi, pattern in enumerate(patterns):
            for ci, char in enumerate(placed):
                if char != UNKNOWN and pattern[ci] != char:
                    patterns[pi] = None
                    break
        patterns = [p for p in patterns if p is not None]

        # find cells that are the same between all possible patterns.
        for c in range(len(placed)):
            if placed[c] != UNKNOWN:
                continue
            possible_cells = set([p[c] for p in patterns])
            if len(possible_cells) == 1:
                placed[c] = list(possible_cells)[0]
        return patterns, placed

    def extract_column(self, col):
        return [row[col] for row in self.chart]

    def return_column(self, col, values):
        for i in range(len(values)):
            row = list(self.chart[i])
            row[col] = values[i]
            self.chart[i] = ''.join(row)

    def solve(self):
        oldChart = None
        newChart = str(self)
        while(oldChart != newChart):
            oldChart = newChart
            for row in range(self.n_rows):
                self.evaluate_row(row)
            for col in range(self.n_cols):
                self.evaluate_col(col)
            newChart = str(self)
        if not self.is_solvable():
            return False
        else:
            return True

    def is_solvable(self):
        return(all(len(patterns) > 0 for patterns in self.row_patterns)
            and all(len(patterns) > 0 for patterns in self.row_patterns))

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.chart])

if __name__ == '__main__':
    solver = Solver('butterfly.txt')
    solver.solve()
    if solver.is_solvable():
        print(str(solver))
    else:
        print('Puzzle is not solvable')
