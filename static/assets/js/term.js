const socket = io("ws://127.0.0.1:5000");
var term = new Terminal();
term.open(document.getElementById('terminal'));
term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')

term.onKey(e => {
    switch (e) {
        case '\u007F': // Backspace (DEL)
            // Do not delete the prompt
            if (term._core.buffer.x > 2) {
                term.write('\b \b');
            }
            break;
        default:
            var f = e.key;
            console.log(f);
            socket.emit("jsrecv", e.key);
    }
});

socket.on('py', (data) => {
    console.log(data);
    term.write(data);
  });
  