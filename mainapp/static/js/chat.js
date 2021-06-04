$(document).ready(function () {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function (data) {
    socket.emit('join');
    fetch('/api/audio')
      .then((res) => res.json())
      .then(function (data) {
        $('.containerr').append(
          `<audio controls src='data:audio/wav;base64,${data.audio}' />`
        );
      });
  });
  socket.on('consultants_join_chat', function (data) {
    loadUsers(data);
  });
  socket.on('user_join_chat', function (data) {
    loadUsers(data);
  });
  socket.on('consultants_work', function (data) {
    loadUsers(data, 1);
  });
  socket.on('server_respone_chat_toUser', function (res) {
    loadChat(res);
  });
  socket.on('server_respone_chat_toConsultant', function (res) {
    loadChat(res);
  });
  function loadChat(res) {
    $('#chat-panel').empty();

    respone = JSON.parse(res);
    data = respone.data;
    target = respone.target;
    console.log(data);

    data.forEach(function (message) {
      const imgTypes = ['image/jpeg', 'image/png'];
      const row = $('<div/>', {
        class: 'row no-gutters'
      });
      if (message.fromUser === target) {
        const col = $('<div/>', {
          class: 'col-md-12'
        });
        row.append(col);
        if (message.content) {
          const bubbleLeft = $('<div/>', {
            class: 'chat-bubble chat-bubble--left',
            text: message.content
          });
          col.append(bubbleLeft);
        }

        if (message.file) {
          if (imgTypes.includes(message.type)) {
            var img = $('<img />', {
              src: message.file,
              class: 'chat-bubble',
              width: 200,
              height: 200
            });
            img.css('float', 'left');
            col.append(img);
          } else {
            col.append(
              `<audio controls class="chat-bubble" style="float: left; width: 300px" src=${message.file} />`
            );
          }
        }
      } else {
        const col = $('<div/>', {
          class: ' offset-md-9 col-md-12'
        });
        row.append(col);
        if (message.content) {
          const bubbleRight = $('<div/>', {
            class: 'chat-bubble chat-bubble--right',
            text: message.content
          });
          col.append(bubbleRight);
        }

        if (message.file) {
          if (imgTypes.includes(message.type)) {
            var img = $('<img />', {
              src: message.file,
              class: 'chat-bubble',
              width: 200,
              height: 200
            });
            img.css('float', 'right');
            col.append(img);
          } else {
            col.append(
              `<audio controls class="chat-bubble" style="float: right; width: 300px" src=${message.file} />`
            );
          }
        }
      }
      $('#chat-panel').append(row);
    });

    //$('#chat-panel').append(`<img src="data:image/gif;base64,${data[0].file}" width="64" height="48"/>`);
    updateScroll();
  }
  function loadUsers(data, isConsultant = 0) {
    $('#friends').empty();
    data.forEach(function (username) {
      const div1 = $('<div/>', {
        class: 'friend-drawer friend-drawer--onhover',
        click: function () {
          $('.current-profile-image').remove();
          $('#currentPeople').prepend(
            `<img class="profile-image current-profile-image" src="https://www.clarity-enhanced.net/wp-content/uploads/2020/06/robocop.jpg"/>`
          );
          $('#currentPeople h6').text(username);
          $('.chat-bubble').hide(0).show(0);
          $('#chatInput').val('');
          if (isConsultant === 1) {
            socket.emit('consultant_load_chat', username);
          } else {
            socket.emit('user_load_chat', username);
          }
        }
      });
      $('#friends').append(div1);
      div1.append(`<img class='profile-image' src='https://www.clarity-enhanced.net/wp-content/uploads/2020/06/robocop.jpg'
                   alt=''>
              <div class="text">
                <h6>${username}</h6>
                <p class='text-muted'></p>
              </div>
              <span class='time text-muted small'>13:21</span>`);
      $('#friends').append('<hr>');
    });
  }
  function updateScroll() {
    var element = document.getElementById('chat-panel');
    element.scrollTop = element.scrollHeight;
  }
  $('#sendButton').click(function () {
    const toUser = $('#currentPeople h6').text();
    const message = $('#chatInput').val();
    const file = document.getElementById('image').files[0];
    if (!toUser || (!message && !file)) return;

    if (file) {
      var fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => {
        var arrayBuffer = fileReader.result;
        const fileObj = {
          name: file.name,
          type: file.type,
          size: file.size,
          binary: arrayBuffer
        };
        socket.emit('send_message', {
          message,
          toUser,
          file: fileObj,
          type: fileObj.type
        });
        document.getElementById('image').value = "";
      };
    } else {
      socket.emit('send_message', {
        message,
        toUser,
        file: { binary: null },
        type: null
      });
    }

    $('#chatInput').val('');
  });
  updateScroll();

  /* ========== RECORD ============  */

  var gumStream;
  //stream from getUserMedia()
  var rec;
  //Recorder.js object
  var input;
  //MediaStreamAudioSourceNode we'll be recording
  // shim for AudioContext when it's not avb.
  var AudioContext = window.AudioContext || window.webkitAudioContext;
  var audioContext = new AudioContext();
  //new audio context to help us record
  var recordButton = document.getElementById('recordButton');
  var stopButton = document.getElementById('stopButton');
//  var pauseButton = document.getElementById('pauseButton');
  //add events to those 3 buttons
  recordButton.addEventListener('click', startRecording);
  stopButton.addEventListener('click', stopRecording);
//  pauseButton.addEventListener('click', pauseRecording);

    stopButton.disabled = true;
    recordButton.disabled = false;
    stopButton.style.display = "none";
    recordButton.style.display = "block";

  function startRecording() {
    /* Simple constraints object, for more advanced audio features see

https://addpipe.com/blog/audio-constraints-getusermedia/ */

    var constraints = {
      audio: true,
      video: false
    };
    /* Disable the record button until we get a success or fail from getUserMedia() */

    recordButton.disabled = true;
    recordButton.style.display = "none";
    stopButton.disabled = false;
    stopButton.style.display = "block";
//    pauseButton.disabled = false;

    /* We're using the standard promise based getUserMedia()

https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function (stream) {
        console.log(
          'getUserMedia() success, stream created, initializing Recorder.js ...'
        );
        /* assign to gumStream for later use */
        gumStream = stream;
        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, {
          numChannels: 1
        });
        //start the recording process
        rec.record();
        console.log('Recording started');
      })
      .catch(function (err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
//        pauseButton.disabled = true;
      });
  }

  function pauseRecording() {
    console.log('pauseButton clicked rec.recording=', rec.recording);
    if (rec.recording) {
      //pause
      rec.stop();
      pauseButton.innerHTML = 'Resume';
    } else {
      //resume
      rec.record();
      pauseButton.innerHTML = 'Pause';
    }
  }
  function stopRecording() {
    console.log('stopButton clicked');
    stopButton.disabled = true;
    recordButton.disabled = false;
    stopButton.style.display = "none";
    recordButton.style.display = "block";
//    pauseButton.disabled = true;
//    pauseButton.innerHTML = 'Pause';
    rec.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    rec.exportWAV(createDownloadLink);
  }
  function createDownloadLink(blob) {
    const toUser = $('#currentPeople h6').text();
    const message = $('#chatInput').val();
    var reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
      var base64String = reader.result;
      console.log('vo roi');
      socket.emit('send_message', {
        message,
        toUser,
        file: { binary: base64String },
        type: blob.type
      });
    };
  }
});
