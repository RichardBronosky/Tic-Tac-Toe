//Objects start here

function Gameboard() {
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

function Player(name, icon) {
  this.name = name;
  this.icon = icon;
  this.gamesWon = 0;
  this.gamesLost = 0;

}

//global variables start here
var winner = false;
var tries = 0;
var playerName = "";
var player1 = new Player("Player 1", "O");
var player2 = new Player("Player 2", "X");
var cpuBool = false;

//non-OOP functions

function checkForWinner(player) {
  var board = new Gameboard();
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
    }
  return winner;
}

function checkForTie(tries, winner) {
  if (tries === 9 && winner === false) {
    $("#winnerdeclaration").text("It's a draw.");
    $(".square").addClass("disableclick");
  }
}

function getRandomInt(num) {
  return Math.floor(Math.random() * (num));
}

function cpuMove() {
  var board = new Gameboard();
  spotsLeft = [];
  for (var i = 0; i <= 8; i++) {
    if ($("#" + i).text() === "") {
      spotsLeft.push("#" + i);
    }
  }
  randomSpot = winComboCheckerFunction(board, player1);
  let randomSpotString = "#" + randomSpot;
  $(randomSpotString).text(player2.icon);
  checkForWinner(player2.icon);
    if (winner === true) {
      $("#winnerdeclaration").text("Machine wins!");
      player2.gamesWon += 1;
      $('#winsPlayer2').text(player2.gamesWon);
      $(".square").addClass("disableclick");
    }
  tries += 1;
}

let winComboCheckerFunction = (board, player) => {
    let win_combos = [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]];
    let arrayed_board = [];
    let block_count = 0;
    let attack_count = 0;
    let block_array = null;
    let attack_array = null;
    let open_spaces = [];
    let win_combos_check_array = [];
    let block_move_open = null;
    for (var key in board) {
        arrayed_board.push(board[key]);
    };
    for (i = 0; i < arrayed_board.length; i++) {
        if (arrayed_board[i] === '') {
            open_spaces.push(i);
        }
    }
    win_combos_check_array = win_combos.map(item => {
        let counter = 0;
        for (i = 0; i < 3; i++) {
            if (arrayed_board[item[i]] === player.icon) {
                counter++;
            } else if (arrayed_board[item[i]] !== player.icon && arrayed_board[item[i]] !== "") {
                counter--;
            }
        }
        return counter;
    });
    for (i = 0; i < win_combos_check_array.length; i++) { //count potential winning combos
        if (win_combos_check_array[i] === 2) {
            block_count++;
        } else if (win_combos_check_array[i] === -2) {
            attack_count++;
        }
    }
    if (attack_count > 0) {
        for (i = 0; i < 8; i++) {
            if (win_combos_check_array[i] === -2) {
                attack_array = win_combos[i];
            }
        }
        for (i = 0; i < 3; i++) {
            if (arrayed_board[attack_array[i]] === '') {
                attack_move_index = i;
            }
        }
        attack_count = 0;
        return attack_array[attack_move_index];
    } else if (block_count >= 1) { //if potential winning combinations number only one, enter this conditional block
        for (i = 0; i < 8; i++) {
            if (win_combos_check_array[i] === 2) {
                block_array = win_combos[i];
            }
        }
        for (i = 0; i < 3; i++) {
            if (arrayed_board[block_array[i]] === '') {
                block_move_index = i;
            }
        }
        block_count = 0;
        return block_array[block_move_index];
    } else {
        block_move_index = open_spaces[Math.floor(Math.random() * (open_spaces.length))];
        return block_move_index;
    }
};

//main jQuery section
$(document).ready(function() {

  $('input:radio').change(
    function(){
        if($(this).val() === 'CPU') {
            $(".square").text("");
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
          playerWin = player1; //can you refactor this section, but putting these variables below?
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
      if (tries < 9 && cpuBool === true && winner === false) {//not registering when cpu wins
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
  $("#winnerdeclaration").text("New Game Started!").delay(2000);
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
