import copy
from collections import Counter

class Sudoku:
    emptyCase = " "

    def __init__(self, data:list) -> None:
        self.hints = [[[] for i in range(0,9)] for j in range(0,9)]
        self.clues = []
        for i in range(0,9):
            s = slice(i*9, i*9 + 9)
            line = [str(x) for x in data[s]]
            for idx, item in enumerate(line):
                if item == "0":
                    line[idx] = self.emptyCase
            self.clues.append(line)
        self.solution = copy.deepcopy(self.clues)
    
    def copy(self):
        s = Sudoku(self.getData())
        s.hints = copy.deepcopy(self.hints)
        return s

    def getData(self):
        out = [n for row in self.solution for n in row]
        return out

    def getRow(self, i: int):
        return self.solution[i]
    
    def getCol(self, j: int):
        return [row[j] for row in self.solution]

    def getBlock(self, i: int, j: int):
        x = slice(int(i/3)*3, int(i/3)*3 + 3)
        y = slice(int(j/3)*3, int(j/3)*3 + 3)
        return sum([row[y] for row in self.solution[x]], [])

    def getRowHint(self, i: int):
        return self.hints[i]
    
    def getColHint(self, j: int):
        return [row[j] for row in self.hints]

    def getBlockHint(self, i: int, j: int):
        x = slice(int(i/3)*3, int(i/3)*3 + 3)
        y = slice(int(j/3)*3, int(j/3)*3 + 3)
        return sum([row[y] for row in self.hints[x]], [])

    def isSolved(self, fast:bool=True):
        if fast:
            return len([x for x in self.solution if self.emptyCase in x]) == 0
        else:
            return len([x for x in self.solution if self.emptyCase in x]) == 0 and self.isValid()

    def showHints(self, hidden=False) -> str:
        out = ""
        for i in range(0,9):
            for j in range(0,9):
                if hidden and self.solution[i][j] != self.emptyCase:
                    out += f'''{i}, {j}: {self.hints[i][j]}\n'''
                elif not hidden and self.solution[i][j] == self.emptyCase:
                    out += f'''{i}, {j}: {self.hints[i][j]}\n'''
        return out

    def isValid(self):
        for n in range(0,9):
            row = Counter(self.getRow(n))
            col = Counter(self.getCol(n))
            block = Counter(self.getBlock(n*3%9, int(n/3)*3))
            for x in range(1,10):
                idx = str(x)
                if row[idx] > 1 or col[idx] > 1 or block[idx] > 1:
                    return False
        return True

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Sudoku):
            return False
        for i in range(0,9):
            for j in range(0,9):
                if self.solution[i][j] != __o.solution[i][j]:
                    return False
        return True

    def __repr__(self) -> str:
        out = ""
        for i in range(0,9):
            line = self.solution[i]
            if i == 3 or i == 6:
                out += "------+-------+------\n"
            out += f'''{line[0]} {line[1]} {line[2]} | {line[3]} {line[4]} {line[5]} | {line[6]} {line[7]} {line[8]}\n'''
        return out
    
