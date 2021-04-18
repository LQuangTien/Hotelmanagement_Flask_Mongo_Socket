$( document ).ready(function() {

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on( 'connect', function(data) {
    socket.emit("join");
  })
  socket.on( 'consultants_join_website', function(data) {
    loadConsultants(data)
  })
  socket.on( 'user_join_chat', function(data) {
    loadConsultants(data)
  })
  function loadConsultants(data) {
      $('#friends').empty();
      data.forEach( function(username) {
        const div1 = $('<div/>', {
            "class": 'friend-drawer friend-drawer--onhover',
            click: function() {
              $('.current-profile-image').remove();
              $('#currentPeople').prepend(`<img class="profile-image current-profile-image" src="https://www.clarity-enhanced.net/wp-content/uploads/2020/06/robocop.jpg"
               alt="">`)
              $('#currentPeople h6').text(username);
              $('.chat-bubble').hide(300).show(200);
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
  updateScroll();
});

