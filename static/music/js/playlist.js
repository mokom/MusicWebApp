var audio;
var playlist;
var tracks;
var current;

//init();
function init() {
    var firstMusic = document.querySelector('#playlist li').firstElementChild.getAttribute('href');
    var audioTag = document.querySelector("#audio-player");
    var sourceTag = document.querySelector('.audio');
    sourceTag.src = firstMusic;
    audioTag.load();
    audioTag.play();

    current = 0;
    audio = $('audio');
    playlist = $('#playlist');
    console.log(playlist);
    tracks = playlist.find('li a');
    len = tracks.length;
    audio[0].volume = .3;
    playlist.find('a').click(function(e){
        e.preventDefault();
        link = $(this);
        console.log("parent");
        console.log( link.parent());
        console.log( link.parent().index());
        current = link.parent().index();
        run(link, audio[0]);
    });
    audio[0].addEventListener('ended',function(e){ // when song has ended
        current++; // take the next song
        if(current == len){
            current = 0;
            link = playlist.find('a')[0];
        }else{
            link = playlist.find('a')[current];
        }
        run($(link),audio[0]);
    });
}

function run(link, player){
        player.src = link.attr('href');
        par = link.parent();
        par.addClass('active').siblings().removeClass('active');
        audio[0].load();
        audio[0].play();
}
