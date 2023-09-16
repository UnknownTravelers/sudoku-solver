from SudokuFileReader import SReader
from SudokuStructures import *
from collections import Counter


def SFindHint(sudoku:Sudoku, x:int, y:int, verbose:bool=False):
    row = sudoku.getRow(x)
    col = sudoku.getCol(y)
    block = sudoku.getBlock(x, y)

    out = [str(x) for x in range(1, 10)
        if str(x) not in col
        and str(x) not in row
        and str(x) not in block]

    if verbose:
        print(x, y, end=" ")
        print("Row:", row, end=" ")
        print("Col:", col, end=" ")
        print("Block:", block, end=" ")
        print("Hints:", out)

    return out

def SFillHints(sudoku:Sudoku, verbose:bool=False):
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku.solution[i][j] == sudoku.emptyCase:
                sudoku.hints[i][j] = SFindHint(sudoku, i, j, verbose=verbose)
            else:
                sudoku.hints[i][j] = []

def SFindAlone(sudoku:Sudoku, x:int, y:int, verbose:bool=False):
    hints = sudoku.hints[x][y]
    row = sudoku.getRowHint(x)
    col = sudoku.getColHint(y)
    block = sudoku.getBlockHint(x, y)
    rowLine = sum(row, [])
    colLine = sum(col, [])
    blockLine = sum(block, [])
    cRow = Counter(rowLine)
    cCol = Counter(colLine)
    cBlock = Counter(blockLine)

    if verbose:
        print(x, y, ":", hints)
        print("cRow:", cRow, end=' ')
        print("cCol:", cCol, end=' ')
        print("cBlock:", cBlock)
        print('---')

    for hint in hints:
        if cRow[hint] == 1:
            return hint
        if cCol[hint] == 1:
            return hint
        if cBlock[hint] == 1:
            return hint

    return None

def SStepOne(sudoku:Sudoku, verbose:bool=False):
    solves = True
    round = 0
    while solves:
        round += 1
        solves = False
        SFillHints(sudoku, verbose=verbose)
        for i in range(0, 9):
            for j in range(0, 9):
                if sudoku.solution[i][j] == sudoku.emptyCase and len(sudoku.hints[i][j]) == 1:
                    solves = True
                    sudoku.solution[i][j] = str(sudoku.hints[i][j][0])
        if verbose:
            print("\nStep 1 Round", round)
            print(sudoku)
        if not sudoku.isValid():
            break

def SStepTwo(sudoku:Sudoku, verbose:bool=False):
    solves = True
    round = 0
    while solves:
        round += 1
        solves = False
        SFillHints(sudoku)
        for i in range(0,9):
            for j in range(0,9):
                if sudoku.solution[i][j] == sudoku.emptyCase:
                    alone = SFindAlone(sudoku, i, j, verbose=verbose)
                    if alone != None:
                        solves = True
                        sudoku.solution[i][j] = str(alone)
        SStepOne(sudoku, verbose=verbose)
        if verbose:
            print("\nStep 2 Round", round)
            print(sudoku)
        if not sudoku.isValid():
            break

def SStepThree(sudoku: Sudoku, verbose: bool=True, depth:int=0):
    # brute force
    if not sudoku.isValid():
        return
    if verbose:
        print(depth)
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku.solution[i][j] == Sudoku.emptyCase:
                if len(sudoku.hints[i][j]) == 0:
                    return
                for n in sudoku.hints[i][j]:
                    s = sudoku.copy()
                    s.solution[i][j] = n
                    if verbose:
                        print(s)
                    SFillHints(s)
                    SStepThree(s, verbose=verbose, depth=depth+1)
                    if s.isSolved() and s.isValid():
                        sudoku.solution = s.solution
                        return
                return

def SSolver(sudoku:Sudoku, verbose:bool=False):
    SStepOne(sudoku, verbose=verbose)
    if verbose:
        print("Step 1:")
        print(sudoku)

    if not sudoku.isValid() or sudoku.isSolved():
        return

    SStepTwo(sudoku, verbose=verbose)
    if verbose:
        print("Step 2:")
        print(sudoku)

    if not sudoku.isValid() or sudoku.isSolved():
        return
    
    SStepThree(sudoku, verbose=verbose)
    if verbose:
        print("Step 3:")
        print(sudoku)
    

if __name__ == "__main__":
    data = SReader("input.txt")
    line = 0
    for table in data:
        line += 1
        sudoku = Sudoku(table)
        print(f"------ BEFORE line {line} ------")
        print(sudoku)
        SSolver(sudoku)
        if not sudoku.isSolved() or not sudoku.isValid():
            if not sudoku.isValid():
                print("INVALID")
            else:
                print("UNSOLVABLE")
        else:
            print(f"------ AFTER line {line} ------")
            print(sudoku)
    