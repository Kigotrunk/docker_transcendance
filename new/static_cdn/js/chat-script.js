const button = document.querySelector('.send-button');
const input = document.querySelector('.text-input');

const talkContainer = document.querySelector('.talk');
talkContainer.scrollTop = talkContainer.scrollHeight;

input.addEventListener('input', () => {
	console.log("change");
	if (input.value === '')
		button.disabled = true;
	else
		button.disabled = false;
});

const showChatList = () => {
	const content = document.querySelector('.content');
	const chatContent = document.createElement('div');
	chatContent.classList.add('chat-content');
  
	fetch('/chat_list')
	  .then(response => response.text())
	  .then(text => {
		const data = JSON.parse(text);
		console.log(data);
		const chatList = document.createElement('div');
		  chatList.classList.add('chat-list');
		  data.conversations.forEach(conversation => {
			  const conversationLink = document.createElement('a');
			  conversationLink.onclick = function () { showChat(conversation.id); };
			  conversationLink.classList.add('chat-user');
			  conversationLink.innerHTML = `
				  <img src="${conversation.other_user.pp}" alt="profile picture">
				  <h4>${conversation.other_user.username}</h4>
				  <div class="overlay"></div>
			  `;
			  chatList.appendChild(conversationLink);
		  });
		content.innerHTML = '';
		chatContent.appendChild(chatList);
		content.appendChild(chatContent);
	});
}

const showChat = (id) => {
	const chatContent = document.querySelector('.chat-content');
	let rightSection = document.querySelector('.chat-right-section');
		if (!rightSection) {
      rightSection = document.createElement('div');
      rightSection.classList.add('chat-right-section');
		}
		else 
      rightSection.innerHTML = '';

	fetch('/get_chat/' + id)
	.then(response => response.text())
	.then(text => {
		const data = JSON.parse(text);
		console.log(data);
		let talkDiv = document.querySelector('.talk');
		if (!talkDiv) {
		talkDiv = document.createElement('div');
		talkDiv.classList.add('talk');
		}
		else 
		talkDiv.innerHTML = '';
		data.messages.forEach(message => {
			const messageDiv = document.createElement('div');
			messageDiv.classList.add('message');
			messageDiv.classList.add(message.issuer === data.uid ? 'received' : 'send');
			messageDiv.textContent = message.message;
			talkDiv.appendChild(messageDiv);
		});
		const messageForm = document.createElement('form');
		messageForm.method = 'POST';
		messageForm.innerHTML = `
		<div class="input">
			<input type=\"text\" name=\"message\" class=\"text-input\" placeholder=\"Type a message\" autocomplete=\"off\" required id=\"id_message\">
			<button type="submit" class="send-button" disabled><span class="material-icons">send</span></button>
		</div>
		`
		rightSection.appendChild(talkDiv);
		rightSection.appendChild(messageForm);
		chatContent.appendChild(rightSection);
		talkDiv.scrollTop = talkDiv.scrollHeight;

		const button = document.querySelector('.send-button');
		const input = document.querySelector('.text-input');
		input.addEventListener('input', () => {
		if (input.value === '')
			button.disabled = true;
		else
			button.disabled = false;
		});
	});
}
