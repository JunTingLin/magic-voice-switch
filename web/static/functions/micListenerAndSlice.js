document.addEventListener('DOMContentLoaded', function() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error("navigator API is not supported");
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            let AudioContext = window.AudioContext || window.webkitAudioContext;
            let audioContext = new AudioContext();
            let source = audioContext.createMediaStreamSource(stream);
            let processor = audioContext.createScriptProcessor(4096, 1, 1);
            source.connect(processor);

            let audioData = [];
            let nextSliceTime = audioContext.currentTime;

            processor.onaudioprocess = function(e) {
                const inputData = e.inputBuffer.getChannelData(0);
                Array.prototype.push.apply(audioData, Array.from(inputData));

                if (audioContext.currentTime >= nextSliceTime) {
                    nextSliceTime += 1;
                    let wavBuffer = encodeWAV(audioData, audioContext.readAudioRate, 1, 16);
                    handleWAVBuffer(wavBuffer); 
                    audioData = []; 
                }
            };
        })
        .catch(err => {
            console.error("microphone access denied/other...", err);
        });
});
