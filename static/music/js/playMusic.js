function Play_Audio(file) {
    var audioTag = document.querySelector('#audio-player');
    var sourceTag = document.querySelector('.audio');
    sourceTag.src = file;
    audioTag.load();
    audioTag.play();
}