try {
	var webSocket = new WebSocket("ws://127.0.0.1:8765");
	console.log("connected to server");
	first_message()
	data_from_server()
} catch {
	alert("unable to connect to the server");
}

function first_message() {
	username = prompt("what is your username ?")
	webSocket.send(`Hello|${username}`)
	display_username(username)
}

function display_username(username) {
	text_field = document.getElementById('username_welcome').innerHTML = `welcome ${username}`
}

function get_input() {
	const data = document.getElementById('user_message');
	send_to_server(data.value)
	data.value = ""
}

function display_message(message) {
	const text_field = document.body.appendChild(document.createElement("p"));
	const text = document.createTextNode(message);
	text_field.appendChild(text);
	text_field.appendChild("");
}

function send_to_server(message) {
	webSocket.send(message)
	data_from_server()
}

function data_from_server() {
	webSocket.onmessage = (event) => {
		display_message(event.data);
	};
}
