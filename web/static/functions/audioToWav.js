//float格式的音訊轉wav檔所加上的header及file format (感謝GPT)
function encodeWAV(readAudio, readAudioRate, numChannels, bitsPerAudio) {
    const buffer = new ArrayBuffer(44 + readAudio.length * 2);
    const view = new DataView(buffer);
    
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + readAudio.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, readAudioRate, true);
    view.setUint32(28, readAudioRate * numChannels * bitsPerAudio / 8, true);
    view.setUint16(32, numChannels * bitsPerAudio / 8, true);
    view.setUint16(34, bitsPerAudio, true);
    writeString(view, 36, 'data');
    view.setUint32(40, readAudio.length * 2, true);

    floatTo16BitPCM(view, 44, readAudio);
    return buffer;
}

function floatTo16BitPCM(output, offset, input) {
    for (let i = 0; i < input.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}

function handleWAVBuffer(buffer) {
    console.log('WAV buffer is ready for further processing');
}
