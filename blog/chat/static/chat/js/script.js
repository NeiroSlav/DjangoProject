// chat.js

function chat_update() {
    $.ajax({
        type: 'GET',
        url: "{% url 'get_chat_messages' %}",
        dataType: 'json',
        data: {
            chat_title: chatName, // Здесь используйте переменную chatName
            user: writer, // Здесь используйте переменную writer
        },
        success: function(response){
            $("#display-chat").empty();

            for (var key in response.messages){
                var temp = response.messages[key].text + "</div>";
                var temp2 = response.messages[key].time + "</div>";

                if (response.messages[key].user == writer) {
                    temp = "<div class='my-chat-message'>" + temp + "<div class='my-chat-time'>" + temp2;
                }
                else {
                    temp = "<div class='chat-message'>" + temp + "<div class='chat-time'>" + temp2;
                }
            $("#display-chat").append(temp);
            }

            var container = document.getElementById("display-chat");
            container.scrollTop = container.scrollHeight;
    });
}

chat_update();

$(document).ready(function () {
    setInterval(function () {
        chat_update();
    }, 1000);
});
