const socket = io("ws://127.0.0.1:5000");
var term = new Terminal();
term.open(document.getElementById('terminal'));
term.onKey(e => {
    switch (e) {
        case '\u007F': // Backspace (DEL)
            // Do not delete the prompt
            if (term._core.buffer.x > 0) {
                term.write('\b \b');
            }
            break;
        default:
            socket.emit("jsrecv", e.key);
    }
});

socket.on('py', (data) => {
    console.log(data);
    term.write(data);
  });


  $('#disconnect').on("click",function(){
    setTimeout(function(){
        window.location.replace("disconnect");
    }, 3000);
});

$('#connect').on("click",function(){
    setTimeout(function(){
        window.location.replace("connect");
    }, 1000);
});