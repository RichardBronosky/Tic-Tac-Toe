
function Gameboard() { //gameboard class for instantiating a gameboard and supplying to gameplay logic
  this.sq1 = $('#0').text();
  this.sq2 = $('#1').text();
  this.sq3 = $('#2').text();
  this.sq4 = $('#3').text();
  this.sq5 = $('#4').text();
  this.sq6 = $('#5').text();
  this.sq7 = $('#6').text();
  this.sq8 = $('#7').text();
  this.sq9 = $('#8').text();
}

function Player(name, icon) { //player class for instantiating player objects
  this.name = name;
  this.icon = icon;
  this.gamesWon = 0;
  this.gamesLost = 0;
}

//globals
var tries = 0; //for draw check
var playerName = ""; //for winner declaration message
var player1 = new Player("Player 1", "O"); //instantiates player 1
var player2 = new Player("Player 2", "X"); //instantiates player 2
var cpuBool = false; //toggles to true when cpu v. machine is selected

//winner check function (this could be made more efficient with a loop); returns true if winner detected
function checkForWinner(player) {
  var board = new Gameboard(); //the current state of the board is assigned to var board
    if (player === board.sq1 && player === board.sq2 && player === board.sq3) {
      winner = true;
    } else if (player === board.sq4 && player === board.sq5 && player === board.sq6) {
      winner = true;
    } else if (player === board.sq7 && player === board.sq8 && player === board.sq9) {
      winner = true;
    } else if (player === board.sq1 && player === board.sq4 && player === board.sq7) {
      winner = true;
    } else if (player === board.sq2 && player === board.sq5 && player === board.sq8) {
      winner = true;
    } else if (player === board.sq3 && player === board.sq6 && player === board.sq9) {
      winner = true;
    } else if (player === board.sq1 && player === board.sq5 && player === board.sq9) {
      winner = true;
    } else if (player === board.sq3 && player === board.sq5 && player === board.sq7) {
      winner = true;
  } else {
      winner = false;
  }
  return winner;
}

//draw check
function checkForTie(tries, winner) {
  if (tries === 9 && winner === false) {
    $("#winnerdeclaration").text("It's a draw.");
    $(".square").addClass("disableclick");
  }
}

//cpu move function
function cpuMove() {
  var board = new Gameboard();
  let cpuSquareSelection = cpuMoveDecider(board, player1);
  let cpuSquareSelectionString = "#" + cpuSquareSelection;
  $(cpuSquareSelectionString).text(player2.icon); //icon added to board
  let winnerCheck = checkForWinner(player2.icon);
    if (winnerCheck === true) {
      $("#winnerdeclaration").text("Machine wins!");
      player2.gamesWon += 1;
      $('#winsPlayer2').text(player2.gamesWon);
      $(".square").addClass("disableclick");
    }
  tries += 1;
}

//AI decision-making function
let cpuMoveDecider = (board, player) => {
    let win_combos = [[0, 1, 2], //array of all possible winning combos
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]];
    let arrayed_board = [];
    let block_count = 0; //keeps a tally of possible winning moves opponent has
    let attack_count = 0; //keeps a tally of possible winning moves cpu has
    let block_array = null; //current opponent winning combination (e.g. [2, 4, 6])
    let attack_array = null; //current cpu winning combination
    let open_spaces = []; //array of all open squares on the board
    let win_combos_check_array = []; //array of scores for each possible scoring combination; index represents each winning combo possibility from win_combos array above. If no gamepiece is placed along a winning combination, the score is zero for that combo; if two gamepieces of the same player are included with the third space open, then the score is a 2.
    for (var key in board) { //loops through gameboard object and pushes values corresponding to the squares on the gameboard to arrayed_board array.
        arrayed_board.push(board[key]);
    };
    for (i = 0; i < arrayed_board.length; i++) {
        if (arrayed_board[i] === '') {
            open_spaces.push(i); //pushes open space indices to open_spaces array
        }
    }
    win_combos_check_array = win_combos.map(item => { //maps over winning combos array and compares each array to the current state of the spaces in that array on the board; scores the array based on the logic below
        let score = 0;
        for (i = 0; i < 3; i++) {
            if (arrayed_board[item[i]] === player.icon) {
                score++;
            } else if (arrayed_board[item[i]] !== player.icon && arrayed_board[item[i]] !== "") {
                score--;
            }
        }
        return score;
    });
    for (i = 0; i < win_combos_check_array.length; i++) { //count potential winning moves of opponent AND cpu
        if (win_combos_check_array[i] === 2) {
            block_count++;
        } else if (win_combos_check_array[i] === -2) {
            attack_count++;
        }
    }

    let board_count = arrayed_board.map(item => { //gets a count of filled spaces on the board
        count = 0;
        if (item !== '') {
            count++;
        }
        return count;
    }).reduce((prev, current) => {
        return prev + current;
    });

    if (board_count === 1) {
        if (arrayed_board[0] !== '') {
            return 8;
        } else if (arrayed_board[2] !== '') {
            return 6;
        } else if (arrayed_board[6] !== '') {
            return 2;
        } else if (arrayed_board[8] !== '') {
            return 0;
        }
    } else if (attack_count > 0) { //if cpu has a winning move, enter this conditional block
        for (i = 0; i < 8; i++) {
            if (win_combos_check_array[i] === -2) {
                attack_array = win_combos[i]; //goes back through win_combos array to pull out the winning combo
            }
        }
        for (i = 0; i < 3; i++) {
            if (arrayed_board[attack_array[i]] === '') {
                attack_move_index = i; //loops through winning combo to identify index within array that is empty
            }
        }
        return attack_array[attack_move_index]; //uses attack_move_index find the actual index of the empty space on the gameboard that leads to a win
    } else if (block_count >= 1) { //defensive check; if opponent has one or more winning moves and cpu doesn't have one, move into this block
        for (i = 0; i < 8; i++) {
            if (win_combos_check_array[i] === 2) {
                block_array = win_combos[i];
            }
        }
        for (i = 0; i < 3; i++) {
            if (arrayed_board[block_array[i]] === '') {
                block_move_index = i; //loops through winning combo to identify index within array that is empty
            }
        }
        return block_array[block_move_index];//uses block_move_index find the actual index of the empty space on the gameboard that leads to a defensive block
    } else {
        block_move_index = open_spaces[Math.floor(Math.random() * (open_spaces.length))];
        return block_move_index; //if neither condition above is met, then cpu moves randomly on the board.
    }
};

//main jQuery section
$(document).ready(function() {

  $('input:radio').change(
    function(){
        if($(this).val() === 'CPU') {
            $(".square").text(""); //resets board if player has already made a move before restarting a game
            cpuBool = true;
            $("#winnerdeclaration").text("Your move!");
            playerIcon = player1.icon;
        } else {
          cpuBool = false;
        }
    }
  );

  var playerIcon = player1.icon;
  $('.square').click(function () {
      $("#winnerdeclaration").text("");
      var squareValue = $(this).text();
      if (squareValue === '') {
        $(this).text(playerIcon);
        checkForWinner(playerIcon);
        if (playerIcon === 'O') {
          playerName = player1.name;
          playerWin = player1;
          playerLose = player2;
          playerIcon = player2.icon;
        } else {
          playerName = player2.name;
          playerWin = player2;
          playerLose = player1;
          playerIcon = player1.icon;
        }
        if (winner === true) {
          $("#winnerdeclaration").text(playerName + " wins!");
          playerWin.gamesWon += 1;
          playerLose.gamesLost += 1;
          $('#winsPlayer1').text(player1.gamesWon);
          $('#winsPlayer2').text(player2.gamesWon);
          $(".square").addClass("disableclick");
        }
      }
      tries += 1;
      checkForTie(tries, winner);
      if (tries < 9 && cpuBool === true && winner === false) {
        $("#winnerdeclaration").text("I'm thinking...");
        setTimeout(function() {
          $("#winnerdeclaration").text("Okay, you're move...");
          cpuMove();
        }, 2000);
        playerIcon = player1.icon;
      }
  }); //end of '.square' click


$('.option-buttons').hide();

$('#restartGame').click(function () {
  winner = false;
  $(".square").removeClass("disableclick");
  $('.square').text('');
  $("#winnerdeclaration").text("New Game Started!");
  playerIcon = player1.icon;
  tries = 0;
});

$('table').click(function () {
  $('tbody').toggle();
});

$('#options').click(function () {
  $('.option-buttons').toggle();
});

$('#clearScoreboard').click(function () {
  player1.gamesWon = 0;
  player2.gamesWon = 0;
  $('#winsPlayer1').text(0);
  $('#winsPlayer2').text(0);
});

}); //end of DOM ready
