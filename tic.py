import random
import contextlib, io

# just a simple tictactoe game with calculated move
# by chandra [perdana1cell@gmail.com]


def MakeListOfFreeFields(board):
    #
    # the function browses the board and builds a list of all the free squares;
    # the list consists of tuples, while each tuple is a pair of row and column numbers
    #
    free = []
    for coordinate in GetCoordinates(board):
        if isinstance(board[coordinate[0]][coordinate[1]], int):
            free.insert(len(free), (coordinate[0], coordinate[1]))
    return free


def VictoryFor(board, sign):
    #
    # the function analyzes the board status in order to check if
    # the player using 'O's or 'X's has won the game
    #
    win = False
    coordinates = GetCoordinates(board)
    for w in MakeListOfWinPaths(board):
        if [
            board[coordinates[w[j] - 1][0]][coordinates[w[j] - 1][1]]
            for j in range(len(board))
        ].count(sign) == len(board):
            win = True
            break
    return win


def MakeListOfDiagonalPaths(board):
    count = len(board)
    diag = []
    diag.insert(len(diag), [i * count + i + 1 for i in range(count)])
    diag.insert(len(diag), [(i + 1) * count - i for i in range(count)])
    return diag


def MakeListOfWinPaths(board):
    count = len(board)
    wins = []
    for i in range(count):
        wins.insert(i, [count * i + j + 1 for j in range(count)])
        wins.insert(len(wins), [count * j + i + 1 for j in range(count)])
    wins = wins + MakeListOfDiagonalPaths(board)
    random.shuffle(wins)
    return wins


def CalculateComputerMove(board, sign="X"):
    if sign == "X":
        inverseSign = "O"
    else:
        inverseSign = "X"

    coordinates = GetCoordinates(board)
    diags = MakeListOfDiagonalPaths(board)
    wins = MakeListOfWinPaths(board)
    poolX, poolO, maxX, maxO = {}, {}, {}, {}
    for i in range(len(wins)):
        path = [
            board[coordinates[wins[i][j] - 1][0]][coordinates[wins[i][j] - 1][1]]
            for j in range(len(board))
        ]
        countX = path.count(sign)
        countO = path.count(inverseSign)

        # remove diagobal yang sudah ada piece(s) lawan
        if countO > 0 and wins[i] in diags:
            diags.remove(wins[i])
        # lanjut iterasi kalau path sudah mati
        if countX > 0 and countO > 0:
            continue
        # kumpulkan path yang berpeluang ditempati
        if countX > 0:
            poolX[i] = countX
            maxX[countX] = list(wins[i])
        # kumpulkan path lawan
        if countO > 0:
            poolO[i] = countO
            maxO[countO] = list(wins[i])

    fields = []
    # kalau pieces imbang atau menang, tambahkan piece di path sendiri
    if len(poolX) > 0 and len(poolO) > 0 and max(maxX) >= max(maxO):
        fields = maxX[max(maxX)]

        # optional : supaya komputer memilih path diagonal bila piece sedang seimbang
        for diag in diags:
            diagPath = [
                board[coordinates[diag[j] - 1][0]][coordinates[diag[j] - 1][1]]
                for j in range(len(board))
            ]
            if diagPath.count(inverseSign) == 0:
                fields = diag
    # kalau pieces lawan lebih baik, tambahkan piece di path lawan
    elif len(poolO) > 0:
        fields = maxO[max(maxO)]

    target = []
    if len(fields) > 0:
        # tempatkan piece di ujung minimal
        if isinstance(
            board[coordinates[min(fields) - 1][0]][coordinates[min(fields) - 1][1]], int
        ):
            target.insert(0, min(fields))
        # atau boleh juga di ujung maksimal
        if isinstance(
            board[coordinates[max(fields) - 1][0]][coordinates[max(fields) - 1][1]], int
        ):
            target.insert(0, max(fields))
        # kalau ujung2 sudah ditempati, tempatkan piece di antaranya
        if len(target) == 0:
            temp = []
            for field in fields:
                if isinstance(
                    board[coordinates[field - 1][0]][coordinates[field - 1][1]], int
                ):
                    temp.insert(0, field)
            target.insert(0, random.choice(temp))

    random.shuffle(target)
    if len(target) > 0:
        return coordinates[target[0] - 1]
    return random.choice(MakeListOfFreeFields(board))


def GetCoordinates(board):
    coordinate = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            coordinate.insert(len(coordinate), (i, j))
    return coordinate


def getBoard(history, cells=3):
    board = [[j + i * cells for j in range(1, 1 + cells)] for i in range(cells)]
    coordinates = GetCoordinates(board)

    for i in range(len(history)):
        if i % 2 == 0:
            sign = "X"
        else:
            sign = "O"

        pos = history[i]
        board[coordinates[pos - 1][0]][coordinates[pos - 1][1]] = sign
    
    return board


def printHistory(history):
    hist = "\n"
    for i in range(len(history)):
        if i % 2 != 0:
            hist += "I chose "
        else:
            hist += "You chose "
        hist += str(history[i]) + "\n"
    return hist


def calculateMove(history, cells=3):
    center = cells * cells // 2 + 1
    if center not in history:
        return center
    else:
        board = getBoard(history)
        return GetCoordinates(board).index(CalculateComputerMove(board, "X")) + 1


def checkState(history, no_of_cell):
    if no_of_cell > 0 and no_of_cell < 10 and no_of_cell not in history:
        # player move
        history.append(no_of_cell)
        victory = checkVictory(getBoard(history), "X")
        if victory != False:
            return {
                "history": history,
                "status": victory,
                "board": DisplayBoard(history, no_of_cell),
            }

        # computer move
        history.append(calculateMove(history))
        victory = checkVictory(getBoard(history), "O")
        if victory != False:
            return {
                "history": history,
                "status": victory,
                "board": DisplayBoard(history, no_of_cell),
            }

    return {
        "history": history,
        "status": None,
        "board": DisplayBoard(history, no_of_cell),
    }


def checkVictory(board, sign):
    if VictoryFor(board, sign):
        if sign == "O":
            return "You lose, {}!"
        else:
            return "Cool, {}!"
    if len(MakeListOfFreeFields(board)) == 0:
        return "Draw, let\'s play again, {}!"
    return False


def DisplayBoard(history, no_of_cell):
    #
    # the function accepts one parameter containing the board's current status
    # and prints it out to the console
    #
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        board = getBoard(history)        
        count = len(board)
        print("", "----" * count, sep="", end="\n")
        for i in range(count):
            print("| ", end="")
            for j in range(count):
                print(
                    "{message:{fill}<{width}}".format(
                        message=board[i][j], width=1, fill=" "
                    ),
                    " | ",
                    sep="",
                    end="",
                )
            print("", end="\n")
            print("", "----" * count, sep="", end="\n")

        print(printHistory(history))

    return f.getvalue()
