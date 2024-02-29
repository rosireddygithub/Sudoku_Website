def generate_combinations(A, B):
    return [a+b for a in A for b in B]

digits = "123456789"
rows = "ABCDEFGHI"
columns = digits
squares = generate_combinations(rows, columns)

unitlist = [generate_combinations(rows, col) for col in columns] + [generate_combinations(row, columns) for row in rows] + [generate_combinations(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

units = dict((square, [unit for unit in unitlist if square in unit]) for square in squares)

peers = dict((square, set(sum(units[square], [])) - set([square])) for square in squares)

class Solver:
    def grid_values(self, grid):
        chars = [char if char in digits or char in '0.' else '123456789' for char in grid]
        return dict(zip(squares, chars))

    def parse_grid(self, grid):
        values = {square: digits for square in squares}
        for s, d in self.grid_values(grid).items():
            if d in digits and not self.assign(values, s, d):
                return False
        return values

    def assign(self, values, square, digit):
        other_values = values[square].replace(digit, '')
        if all(self.eliminate(values, square, d2) for d2 in other_values):
            return values
        return False

    def eliminate(self, values, s, d):
        if d not in values[s]:
            return values
        values[s] = values[s].replace(d, '')
        if len(values[s]) == 0:
            return False
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all(self.eliminate(values, s2, d2) for s2 in peers[s]):
                return False
        for unit in units[s]:
            dplaces = [s for s in unit if d in values[s]]
            if len(dplaces) == 0:
                return False
            elif len(dplaces) == 1:
                if not self.assign(values, dplaces[0], d):
                    return False
        return values

    def search(self, values):
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in squares):
            return values
        n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
        return self.some(self.search(self.assign(values.copy(), s, d)) for d in values[s])

    def solve(self, grid):
        return self.search(self.parse_grid(grid))

    def some(self, seq):
        for e in seq:
            if e:
                return e
        return False

    def solved(self, puzzle):
        values = dict(zip(squares, puzzle))
        return values is not False and all(set(values[s] for s in unit) == set(digits) for unit in unitlist)
