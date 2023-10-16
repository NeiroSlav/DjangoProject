var last_message_id = 0;
var chatName = document.querySelector(".opened-chat").getAttribute("data-chat-name");
var writer = document.querySelector(".opened-chat").getAttribute("data-writer");
var chatUrl = document.querySelector(".opened-chat").getAttribute("data-chat-url");


function chat_update() {
    $.ajax({
        type: 'GET',
        url : chatUrl,
        dataType: 'json',
        data: {
        chat_title: chatName,
        },

        success: function(response){
            if (last_message_id != response.last_message_id) {
                last_message_id = response.last_message_id;

                var container = document.getElementById("display-chat");
                $(container).empty();

                for (var key in response.messages){
                    var temp = response.messages[key].text + "</div>";
                    var temp2 = response.messages[key].time + "</div>";

                    if (response.messages[key].user == writer) {
                        temp = "<div class='my-chat-message'>" + temp + "<div class='my-chat-time'>" + temp2;
                    }
                    else {
                        temp = "<div class='chat-message'>" + temp + "<div class='chat-time'>" + temp2;
                    }
                $(container).append(temp);
                }

            }

            container.scrollTop = container.scrollHeight;
        }
    });
}

chat_update()

window.onload = function() {
    var inputElement = document.getElementById("chat-input");

    if (inputElement) {
        inputElement.focus();
    }
};

$(document).ready(function(){
    setInterval(function(){
    chat_update();
    },1000);
});