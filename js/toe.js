// Setting my Globals, seeing what I need and what I don't

// First I grab my DOM elements
var cubes = document.getElementsByClassName("myCube");
var state = [0,0,0,0,0,0,0,0,0];
var game = true;

var myButtons = document.getElementsByClassName("myButton");
var board = document.getElementsByClassName("board");



// Setting up my 'light switches'
var humanPlayer = false;
var computerPlayer = true;
var humanPlayerTurn = -1;
var computerPlayerTurn = 1;

var playerWins = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function restartMyGame() {
    for (var x = 0; x < 9; x++) {
        cubes[x].style.background = "#fff";
        state[x] = 0;
    }

    for (var x = 0; x < 2; x++) {
        myButtons[x].style.margin = "0.2vh";
        myButtons[x].style.opacity = "1";
        myButtons[x].style.width = "15.5vh";
    }

    game = true;
}

function myVar(clicked)
{
    if (!game)
        return;

    for (var x = 0; x < 9; x++)
    {
        if (cubes[x] == clicked && state[x] == 0)
        {
            play(x, humanPlayer);
            computerBehavior();
        }
    }
}

// Winning matrix (I had to look this up), all possible
// winning positions

function play(index, player)
{
    if (!game)
        return;

    if (state[index] == 0)
    {
        myButtons[0].style.width = "0";
        myButtons[0].style.margin = "0";
        myButtons[0].style.opacity = "0";

        myButtons[1].style.width = "32vh";
        if (player == humanPlayer)
        {
            cubes[index].style.backgroundImage = "url('img/cross.png')";
            cubes[index].style.backgroundRepeat = "no-repeat";
            state[index] = humanPlayerTurn;
        }
        else
        {
            cubes[index].style.backgroundImage = "url('img/Circle.png')";
            cubes[index].style.backgroundRepeat = "no-repeat";
            state[index] = computerPlayerTurn;
        }

        if (checkWin(state, player))
            game = false;
    }
}

function checkWin(board, player)
{
    var value = player = humanPlayer ? humanPlayerTurn : computerPlayerTurn;

    for (var x = 0; x < 8; x++)
    {
        var win = true;

        for (var y = 0; y < 3; y++)
        {
            if (board[playerWins[x][y]] != value)
            {
                win = false;
                break;
            }
        }

        if (win)
            return true;
    }

    return false;
}

function checkFull(board)
{
    for (var x = 0; x < 9; x++)
    {
        if (board[x] == 0)
            return false;

    }
    return true;
}

function computerBehavior() {
    callComputer(state, 0, computerPlayer);
}

function callComputer(board, depth, player)
{
    if (checkWin(board, !player))
        return -10 + depth;

    if (checkFull(board))
        return 0;

    var value = player == humanPlayer ? humanPlayerTurn : computerPlayerTurn;

    var max = -Infinity;
    var index = 0;

    for (var x = 0; x < 9; x++)
    {
        if (board[x] == 0)
        {
            var newboard = board.slice();
            newboard[x] = value;

            var moveval = -callComputer(newboard, depth + 1, !player);

            if (moveval > max)
            {
                max = moveval;
                index = x;
            }
        }
    }

    if(depth == 0)
        play(index, computerPlayer);

        return max;
}
