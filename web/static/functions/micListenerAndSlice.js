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
            let isProcessing = false;

            processor.onaudioprocess = function(e) {
                if (isProcessing) return; // 如果正在處理，則跳過這次事件
                
                const inputData = e.inputBuffer.getChannelData(0);
                audioData.push(...inputData);

                if (audioContext.currentTime >= nextSliceTime) {
                    nextSliceTime += 1;
                    let wavBuffer = encodeWAV(audioData, audioContext.sampleRate, 1, 16);
                    isProcessing = true;
                    sendWAVBufferToServer(wavBuffer).then(() => {
                        audioData = [];
                        setTimeout(() => {
                            isProcessing = false;
                        }, 500); // 0.5秒的延遲
                    });
                }
            };

            processor.connect(audioContext.destination);
        })
        .catch(function(err) {
            console.error("microphone access denied/other...", err);
        });
});

function sendWAVBufferToServer(buffer) {
    return new Promise((resolve, reject) => {
        let blob = new Blob([buffer], { type: 'audio/wav' });
        let formData = new FormData();
        formData.append('file', blob, 'output.wav');

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                console.log('WAV file sent to server');
                resolve();
            } else {
                console.error('Failed to send WAV file to server');
                reject();
            }
        }).catch(error => {
            console.error('Error sending WAV file to server:', error);
            reject();
        });
    });
}
