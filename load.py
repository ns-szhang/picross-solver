"""Load picross puzzle data from hanjie-star.com"""

import requests
import re
from picross import Solver

puzzle_name = 'fidel-castro-death-18672'
url = 'http://www.hanjie-star.com/picross/{}.html'.format(puzzle_name)

page = requests.get(url)
content = str(page.content)

row_matches = re.search('trows: "([^"]*)"', content)
rows = row_matches.group(1).split(';')
rows = [' '.join(row.split(',')) for row in rows]
col_matches = re.search('tcols: "([^"]*)"', content)
cols = col_matches.group(1).split(';')
cols = [' '.join(col.split(',')) for col in cols]

filename = '{}.txt'.format(puzzle_name)
with open(filename, 'w') as file:
    file.write('{} {}\n\n'.format(len(cols), len(rows)))
    for col in cols:
        file.write(col + '\n')
    file.write('\n')
    for row in rows:
        file.write(row + '\n')

solver = Solver(filename)
solver.solve()
if solver.is_solvable():
    print(str(solver))
else:
    print('Puzzle is not solvable')
