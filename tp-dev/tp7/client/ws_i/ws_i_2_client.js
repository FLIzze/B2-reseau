try {
	webSocket = new WebSocket("ws://127.0.0.1:8765");
} catch {
	alert("unable to connect to the server")
}

try {
	input = prompt("input");
	webSocket.send(input);
	webSocket.onmessage = (event) => {
		alert(event.data);
	};
} catch {
	alert("cant retrieve data from server")
}
