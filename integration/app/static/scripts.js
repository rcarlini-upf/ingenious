window.addEventListener('load', (event) => {

  //webkitURL is deprecated but nevertheless 
  URL = window.URL || window.webkitURL;

  var gumStream;
  //stream from getUserMedia() 
  var rec;
  //Recorder.js object 
  var input;

  var formData;

  //MediaStreamAudioSourceNode we'll be recording 
  // shim for AudioContext when it's not avb. 
  var AudioContext = window.AudioContext || window.webkitAudioContext;
  var audioContext = new AudioContext;

  //new audio context to help us record 
  var startButton = document.getElementById("startButton");
  var stopButton = document.getElementById("stopButton");
  var sendButton = document.getElementById("sendButton");
  var audioPlayer = document.getElementById("recording");
  let logElement = document.getElementById("log");

  //add events to those 3 buttons 
  startButton.addEventListener("click", startRecording);
  stopButton.addEventListener("click", stopRecording);
  sendButton.addEventListener("click", postWav);

  function startRecording() {

    console.log("startButton clicked");

    var constraints = {
      audio: true,
      video: false
    }
    /* Disable the record button until we get a success or fail from getUserMedia() */

    startButton.disabled = true;
    stopButton.disabled = false;
    sendButton.disabled = false

    /* We're using the standard promise based getUserMedia()
    
    https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */

    navigator.mediaDevices.getUserMedia(constraints)
      .then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        /* assign to gumStream for later use */
        gumStream = stream;
        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);
        /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
        rec = new Recorder(input, {
          numChannels: 1
        })
        //start the recording process 
        rec.record()
        console.log("Recording started");

      }).catch(function (err) {
        //enable the record button if getUserMedia() fails 
        startButton.disabled = false;
        stopButton.disabled = true;
        sendButton.disabled = true
      });
  }

  function stopRecording() {
    console.log("stopButton clicked");
    //disable the stop button, enable the record too allow for new recordings 
    stopButton.disabled = true;
    startButton.disabled = false;
    sendButton.disabled = false;

    //tell the recorder to stop the recording 
    rec.stop(); //stop microphone access 
    gumStream.getAudioTracks()[0].stop();

    rec.exportWAV(blob => {
      audioPlayer.src = URL.createObjectURL(blob);
      downloadButton.href = audioPlayer.src;
      downloadButton.download = "recorded.wav";

      formData = new FormData();
      formData.append('audio', blob, "recorded.wav");
    });
  }

  function log(msg) {
    logElement.innerHTML += msg + "\n";
  }

  function postWav() {

    $.ajax({
      type: 'POST',
      url: '/process_audio',
      data: formData,
      processData: false,
      contentType: false
    }).done(function (data) {
      console.log(data);
      log("Speech-to-text output: " + data.text);
    });

  };

});