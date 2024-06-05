document.addEventListener('DOMContentLoaded', function() {
    // check whether necessary functions are supported in user's browser
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error("getUserMedia function is not supported");
        return;
    }

    const handleMic = (stream) => {
        let AudioContext = window.AudioContext || window.webkitAudioContext;
        let audioContext = new AudioContext();
        
        // create a source node from the stream
        microphone = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        
        // connect the microphone to the analyser
        microphone.connect(analyser);
        
        // log to indicate that the microphone is now listening
        console.log("microphone is listening...");
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(handleMic)
        .catch(function(err) {
            // access denied or other error
            console.error("microphone access denied/ other...", err);
        });
});
