const height = 600;
const width = 800;

function gameSection() {

	const gameSocket = new WebSocket('ws://' + window.location.host + `/ws/pong/`);

	const content = document.querySelector('.content');
	content.innerHTML = `
		<div id="game-container">
			<div id="score"></div>
			<canvas id="pongCanvas" width="${width}" height="${height}"></canvas>
			<div id="pong-menu"></div>
		</div>
	`;

	const canvas = document.getElementById('pongCanvas');
	const ctx = canvas.getContext('2d');
	ctx.fillStyle = "white";
	const scoreDiv = document.getElementById('score');
	let gameStarted = false;

	const showGameMenu = () => {
		console.log('menu');
		const pongMenu = document.getElementById('pong-menu');
	
		const button1 = document.createElement('button');
		button1.innerHTML = 'Play Online';
		button1.onclick = () => joinRoom('pvp', 'room1'); // (ajouter matchmaking / jouer avec ami)
		pongMenu.appendChild(button1);
	
		const button2 = document.createElement('button');
		button2.innerHTML = 'Play with a friend';
		button2.onclick = () => selectRoom();
		pongMenu.appendChild(button2);
	
		const button3 = document.createElement('button');
		button3.innerHTML = 'Ai Mode';
		button3.onclick = () => versusAi();
		pongMenu.appendChild(button3);
	}
	showGameMenu();

	gameSocket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		console.log(data);
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

	gameSocket.onopen = function(e) {
		console.error('gameSocket opened');
	};

	gameSocket.onclose = function(e) {
		console.error('gameSocket closed unexpectedly');
	};
	
	let up = false;
	let down = false;

    function sendInput(dir) {
		if (!gameStarted)
			return;
        gameSocket.send(JSON.stringify({
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
		if ('game_over' in gameState && gameState['game_over'] == true)
				return gameOver(gameState);
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawBall(gameState.ball_position);
		ctx.fillRect(0, gameState.paddle1_position, 10, 80);
		ctx.fillRect(790, gameState.paddle2_position, 10, 80);
		if ('score' in gameState)
			scoreDiv.innerText = `${gameState.score[0]} - ${gameState.score[1]}`;
		else if ('surv_score' in gameState)
			scoreDiv.innerText = gameState['surv_score']
	}

	function drawBall(position) {
		ctx.beginPath();
		ctx.arc(position[0], position[1], 10, 0, Math.PI * 2);
		ctx.fill();
	}

	window.addEventListener('blur', function() {
		sendInput(0);
	});

	const versusAi = () => {
		const pongMenu = document.getElementById('pong-menu');
		pongMenu.innerHTML = '';
	
		const button1 = document.createElement('button');
		button1.innerHTML = 'Easy';
		button1.onclick = () => joinRoom('ai', 1);
		pongMenu.appendChild(button1);
	
		const button2 = document.createElement('button');
		button2.innerHTML = 'Medium';
		button2.onclick = () => joinRoom('ai', 2);
		pongMenu.appendChild(button2);
	
		const button3 = document.createElement('button');
		button3.innerHTML = 'Hard';
		button3.onclick = () => joinRoom('ai', 3);
		pongMenu.appendChild(button3);
	
		const button4 = document.createElement('button');
		button4.innerHTML = 'Survival';
		button4.onclick = () => joinRoom('ai', 4);
		pongMenu.appendChild(button4);
	}
	
	const selectRoom = () => {
		const pongMenu = document.getElementById('pong-menu');
		pongMenu.innerHTML = '';
	
		const button1 = document.createElement('button');
		button1.innerHTML = 'test 1';
		button1.onclick = () => joinRoom('pvp', 'test 1');
		pongMenu.appendChild(button1);
	
		const button2 = document.createElement('button');
		button2.innerHTML = 'test 2';
		button2.onclick = () => joinRoom('pvp', 'test 2');
		pongMenu.appendChild(button2);
	
		const input = document.createElement('input');
		const sendButton = document.createElement('button');
		input.addEventListener('keydown', (event) => {
			if (event.key === 'Enter') {
				joinRoom('pvp', input.value);
			}
		});
		sendButton.innerHTML = '<span class="material-icons">send</span>';
		sendButton.onclick = () => joinRoom('pvp', input.value);
		pongMenu.appendChild(input);
		pongMenu.appendChild(sendButton);
	}
	
	const joinRoom = (mode, roomName) => {
		console.log(`join in ${mode} room : ${roomName}`);
		gameSocket.send(JSON.stringify({
			'action': 'join',
			'mode': mode,
			'room': roomName
		}));
		document.getElementById('pong-menu').innerHTML = '';
	}
	
	const gameOver = (gameState) => {
		const pongMenu = document.getElementById('pong-menu');
		const gameOverDiv = document.createElement('div');
		gameOverDiv.id = 'game-over';
		const spanElement = document.createElement('span');
		spanElement.textContent = 'GAME OVER';
		gameOverDiv.appendChild(spanElement);
		pongMenu.appendChild(gameOverDiv);

		const buttonDiv = document.createElement('div');
		const retryButton = document.createElement('button');
		retryButton.innerHTML = 'Retry';
		retryButton.onclick = () => joinRoom('ai', 4);
		retryButton.classList.add('primary-btn')
		const mainMenu = document.createElement('button');
		mainMenu.innerHTML = 'Return Menu';
		mainMenu.onclick = () => showGameMenu(); 
		mainMenu.classList.add('secondary-btn')
		buttonDiv.appendChild(retryButton);
		buttonDiv.appendChild(mainMenu);
		gameOverDiv.appendChild(buttonDiv);
	}
}
