$( document ).ready(function() {

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on( 'connect', function(data) {
    socket.emit("join");
  })
  socket.on( 'consultants_join_chat', function(data) {
    loadUsers(data)
  })
  socket.on( 'user_join_chat', function(data) {
    loadUsers(data)
  })
  socket.on('consultants_work', function(data){
    loadUsers(data, 1)
  })
  socket.on( 'server_respone_chat_toUser', function(res) {
    loadChat(res)
  })
  socket.on( 'server_respone_chat_toConsultant', function(res) {
    loadChat(res)
  })
  function loadChat(res) {
      $('#chat-panel').empty();

      respone = JSON.parse(res);
      data = respone.data;
      target = respone.target;
      data.forEach(function(message){
        const row = $('<div/>', {
              "class": 'row no-gutters',
        })
        if(message.fromUser === target) {
           const col = $('<div/>', {
                "class": 'col-md-12',
          })
          row.append(col)
           const bubbleLeft = $('<div/>', {
              "class": 'chat-bubble chat-bubble--left',
              text: message.content
          })
          col.append(bubbleLeft)
        } else {
         const col = $('<div/>', {
                "class": ' offset-md-9 col-md-12',
          })
          row.append(col)
          const bubbleRight = $('<div/>', {
              "class": 'chat-bubble chat-bubble--right',
              text: message.content
          })
          col.append(bubbleRight)
        }
        $('#chat-panel').append(row);
      })
      updateScroll();
  }
  function loadUsers(data, isConsultant = 0) {
      $('#friends').empty();
      data.forEach( function(username) {
        const div1 = $('<div/>', {
            "class": 'friend-drawer friend-drawer--onhover',
            click: function() {
              $('.current-profile-image').remove();
              $('#currentPeople').prepend(`<img class="profile-image current-profile-image" src="https://www.clarity-enhanced.net/wp-content/uploads/2020/06/robocop.jpg"/>`)
              $('#currentPeople h6').text(username);
              $('.chat-bubble').hide(0).show(0);
              $('#chatInput').val('')
              if(isConsultant === 1){
                socket.emit( 'consultant_load_chat', username)
              } else {
                socket.emit( 'user_load_chat', username)
              }

            }
        })
        $('#friends').append(div1)
        div1.append(`<img class='profile-image' src='https://www.clarity-enhanced.net/wp-content/uploads/2020/06/robocop.jpg'
                   alt=''>
              <div class="text">
                <h6>${username} (Online)</h6>
                <p class='text-muted'>Hey, you're arrested!</p>
              </div>
              <span class='time text-muted small'>13:21</span>`
        )
        $('#friends').append('<hr>')
      })
  }
  function updateScroll(){
    var element = document.getElementById("chat-panel");
    element.scrollTop = element.scrollHeight;
  }
  $('#sendButton').click(function(){
    const toUser = $('#currentPeople h6').text();
    const message = $('#chatInput').val();
    if(!toUser || !message) return;
    socket.emit('send_message', {message, toUser})
    $('#chatInput').val('')
  });
  updateScroll();
});

