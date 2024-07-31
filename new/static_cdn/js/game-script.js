const height = 600;
const width = 800;

const content = document.querySelector('.content');

function displayRooms() {
	content.innerHTML = `
		<div id="game-container">
			<div id="score"></div>
			<canvas id="pongCanvas" width="${width}" height="${height}"></canvas>
			<div id="pong-menu"></div>
		</div>
	`;

	const socket = new WebSocket(
		'ws://' + window.location.host + `/ws/pong/`
	);

	const canvas = document.getElementById('pongCanvas');
	const ctx = canvas.getContext('2d');
	ctx.fillStyle = "white";
	const scoreDiv = document.getElementById('score');
	let gameStarted = false;

	const pongMenu = document.getElementById('pong-menu');

	const button1 = document.createElement('button');
	button1.innerHTML = 'Play Online';
	button1.onclick = () => joinRoom(socket, 'pvp', 'room1'); // (ajouter matchmaking / jouer avec ami)
	pongMenu.appendChild(button1);

	const button2 = document.createElement('button');
	button2.innerHTML = 'Play with a friend';
	button2.onclick = () => selectRoom(socket);
	pongMenu.appendChild(button2);

	const button3 = document.createElement('button');
	button3.innerHTML = 'Ai Mode';
	button3.onclick = () => versusAi(socket);
	pongMenu.appendChild(button3);

	socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		if ('countdown' in data) {
			scoreDiv.innerText = data['countdown'];
			if (data['countdown'] === "") {
				gameStarted = true;
				scoreDiv.innerText = "0 - 0";
			}
		} else if ('waiting' in data && data['waiting'] === false) {
			// Mettre à jour l'affichage lorsque les deux joueurs sont connectés
			scoreDiv.innerText = "0 - 0";
		} else {
			updateGameState(data);
		}
	};

	socket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};
	
	let up = false;
	let down = false;

    function sendInput(dir) {
		if (!gameStarted)
			return;
        socket.send(JSON.stringify({
			'action': 'move',
			'direction': dir,
		}));
	}

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowUp' && up === false) {
            up = true;
			sendInput(up - down);
        }
		else if (event.key === 'ArrowDown' && down === false) {
            down = true;
			sendInput(up - down);
        }
    });

    document.addEventListener('keyup', (event) => {
		if (event.key === 'ArrowUp') {
            up = false;
			sendInput(up - down);
        }
		else if (event.key === 'ArrowDown') {
            down = false;
			sendInput(up - down);
        }
    });

	function updateGameState(gameState) {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawBall(gameState.ball_position);
		ctx.fillRect(0, gameState.paddle1_position, 10, 80);
		ctx.fillRect(790, gameState.paddle2_position, 10, 80);
		scoreDiv.innerText = `${gameState.score[0]} - ${gameState.score[1]}`;
	}

	function drawBall(position) {
		ctx.beginPath();
		ctx.arc(position[0], position[1], 10, 0, Math.PI * 2);
		ctx.fill();
	}

	window.addEventListener('blur', function() {
		sendInput(0);
	});
}


function versusAi(socket) {
	const pongMenu = document.getElementById('pong-menu');
	pongMenu.innerHTML = '';

	const button1 = document.createElement('button');
	button1.innerHTML = 'Easy';
	button1.onclick = () => joinRoom(socket, 'ai', 1);
	pongMenu.appendChild(button1);

	const button2 = document.createElement('button');
	button2.innerHTML = 'Medium';
	button2.onclick = () => joinRoom(socket, 'ai', 2);
	pongMenu.appendChild(button2);

	const button3 = document.createElement('button');
	button3.innerHTML = 'Hard';
	button3.onclick = () => joinRoom(socket, 'ai', 3);
	pongMenu.appendChild(button3);

	const button4 = document.createElement('button');
	button4.innerHTML = 'Survival';
	button4.onclick = () => joinRoom(socket, 'ai', 4);
	pongMenu.appendChild(button4);
}

function selectRoom (socket) {
	const pongMenu = document.getElementById('pong-menu');
	pongMenu.innerHTML = '';

	const button1 = document.createElement('button');
	button1.innerHTML = 'test 1';
	button1.onclick = () => joinRoom(socket, 'pvp', 'test 1');
	pongMenu.appendChild(button1);

	const button2 = document.createElement('button');
	button2.innerHTML = 'test 2';
	button2.onclick = () => joinRoom(socket, 'pvp', 'test 2');
	pongMenu.appendChild(button2);

	const input = document.createElement('input');
	const sendButton = document.createElement('button');
	input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') {
			joinRoom(socket, 'pvp', input.value);
		}
	});
	sendButton.innerHTML = '<span class="material-icons">send</span>';
	sendButton.onclick = () => joinRoom(socket, 'pvp', input.value);
	pongMenu.appendChild(input);
	pongMenu.appendChild(sendButton);
}

function joinRoom(socket, mode, roomName) {
	console.log(`join in ${mode} room : ${roomName}`);
	socket.send(JSON.stringify({
		'action': 'join',
		'mode': mode,
		'room': roomName
	}));
	document.getElementById('pong-menu').innerHTML = '';
}
