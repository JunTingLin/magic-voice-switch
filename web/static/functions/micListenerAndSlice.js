$(document).ready(function() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error("navigator API is not supported");
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            let AudioContext = window.AudioContext || window.webkitAudioContext;
            let audioContext = new AudioContext();
            let source = audioContext.createMediaStreamSource(stream);
            let processor = audioContext.createScriptProcessor(4096, 1, 1);
            source.connect(processor);

            let audioData = [];
            let nextSliceTime = audioContext.currentTime;

            processor.onaudioprocess = function(e) {
                const inputData = e.inputBuffer.getChannelData(0);
                audioData.push(...inputData);

                if (audioContext.currentTime >= nextSliceTime) {
                    nextSliceTime += 1;
                    let wavBuffer = encodeWAV(audioData, audioContext.sampleRate, 1, 16);
                    saveWAVBuffer(wavBuffer, 'output.wav');
                    audioData = [];
                }
            };

            processor.connect(audioContext.destination);
        })
        .catch(function(err) {
            console.error("microphone access denied/other...", err);
        });
});

function saveWAVBuffer(buffer, filename) {
    let blob = new Blob([buffer], { type: 'audio/wav' });
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}
