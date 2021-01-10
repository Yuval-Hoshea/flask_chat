let activeUser, username, message, datetime;
const socket = io.connect(url["url"]);


function addMessage(data){
    //add new message
    let table = document.getElementById("chatTable");
    let tr = document.createElement("tr");
    const className = (data["username"] == activeUser)? "userMsg" : "otherMsg";
    let trHtml = `<tr>
                    <td class="${className}">
                        <p class="msgInfo">${data["username"]} at ${data["datetime"]}</p>
                        <p>${data["message"]}</p>
                    </td>
                </tr>`;
    // trHtml = "<td><b>" + data["username"] +"</b></td>";
    // trHtml += "<td><b>" + data["datetime"]+ "</b></td>";
    // trHtml += "<td>" + data["message"] + "</td>";
    tr.innerHTML = trHtml;
    table.appendChild(tr);
}


function removeAndAddAgain() {
    let table = document.getElementById("chatTable");
    let userInput = document.getElementById("text");
    userInput.remove();
    table.appendChild(userInput);
}


socket.on('recieveMessage', function(data){
    console.log("on event!");
    addMessage(data);
    removeAndAddAgain();
    document.getElementById("userInput").focus(); //focus on the text bar
});


function onSubmit() {
    let message = document.getElementById("userInput").value;
    
    if (message != "") {
        console.log("submit!");
        socket.emit('newMessage', {"message": message});
        document.getElementById("userInput").value = "";
    }
}