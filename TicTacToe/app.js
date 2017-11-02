var tttBoard;
var human = 'O';
var ai = 'X';
var winArr = [[0, 3, 6],[1, 4, 7],[3, 4, 5],[6, 7, 8],[0, 1, 2],[0, 4, 8],[2, 5, 8],[6, 4, 2]]

var boxs = document.querySelectorAll('.box');
startTTT();

function startTTT() {
	document.querySelector(".finished").style.display = "none";
	tttBoard = Array.from(Array(9).keys());
	for (var i = 0; i < boxs.length; i++) {
		boxs[i].innerText = '';
		boxs[i].style.removeProperty('background-color');
		boxs[i].addEventListener('click', firstMove, false);
	}
}
function symbolSelect(value) {
	if (value === "Cross") {
		human = "X";
		ai = "O";
	} else {
		human = "O";
		ai = "X";
	}
}

function firstMove(square) {
	if (typeof tttBoard[square.target.id] == 'number') {
		turn(square.target.id, human)
		if (!winChecker(tttBoard, human) && !isTie()) turn(logicalPlace(), ai);
	}
}

function turn(recNum, player) {
	tttBoard[recNum] = player;
	document.getElementById(recNum).innerText = player;
	let wonTheGame = winChecker(tttBoard, player)
	if (wonTheGame) endOfG(wonTheGame)
}

function winChecker(board, player) {
	let plays = board.reduce((a, e, i) =>
		(e === player) ? a.concat(i) : a, []);
	let wonTheGame = null;
	for (let [index, win] of winArr.entries()) {
		if (win.every(elem => plays.indexOf(elem) > -1)) {
			wonTheGame = {index: index, player: player};
			break;
		}
	}
	return wonTheGame;
}

function endOfG(wonTheGame) {
	for (let index of winArr[wonTheGame.index]) {
		document.getElementById(index).style.backgroundColor =
			wonTheGame.player == human ? "blue" : "red";
	}
	for (var i = 0; i < boxs.length; i++) {
		boxs[i].removeEventListener('click', firstMove, false);
	}
	ForTheWin(wonTheGame.player == human ? "You win!" : "You lose!");
}

function ForTheWin(who) {
	document.querySelector(".finished").style.display = "block";
	document.querySelector(".finished .text").innerText = who;
}

function cleared() {
	return tttBoard.filter(s => typeof s == 'number');
}

function logicalPlace() {
	return minimax(tttBoard, ai).index;
}

function isTie() {
	if (cleared().length == 0) {
		for (var i = 0; i < boxs.length; i++) {
			boxs[i].style.backgroundColor = "green";
			boxs[i].removeEventListener('click', firstMove, false);
		}
		ForTheWin("Tie Game!")
		return true;
	}
	return false;
}

function minimax(newTTT, player) {
	var remaining = cleared(newTTT);

	if (winChecker(newTTT, human)) {
		return {score: -10};
	} else if (winChecker(newTTT, ai)) {
		return {score: 10};
	} else if (remaining.length === 0) {
		return {score: 0};
	}
	var moves = [];
	for (var i = 0; i < remaining.length; i++) {
		var move = {};
		move.index = newTTT[remaining[i]];
		newTTT[remaining[i]] = player;

		if (player == ai) {
			var result = minimax(newTTT, human);
			move.score = result.score;
		} else {
			var result = minimax(newTTT, ai);
			move.score = result.score;
		}

		newTTT[remaining[i]] = move.index;

		moves.push(move);
	}

	var finishingTouch;
	if(player === ai) {
		var record = -10000;
		for(var i = 0; i < moves.length; i++) {
			if (moves[i].score > record) {
				record = moves[i].score;
				finishingTouch = i;
			}
		}
	} else {
		var record = 10000;
		for(var i = 0; i < moves.length; i++) {
			if (moves[i].score < record) {
				record = moves[i].score;
				finishingTouch = i;
			}
		}
	}

	return moves[finishingTouch];
}
