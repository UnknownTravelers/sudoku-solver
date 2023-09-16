def SReader(fileName):
    data = []

    with open(fileName, 'r', encoding='utf-8') as inputFile:
        for line in inputFile:
            data.append([i for i in line[:-1]])
    return data

if __name__ == "__main__":
    from SudokuStructures import Sudoku
    table = SReader("input.txt")[0]
    sudoku = Sudoku(table)
    print(sudoku)