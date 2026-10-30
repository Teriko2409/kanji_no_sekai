const music = document.getElementById("theme");

if (music) {
    music.volume = 0.30;
    music.loop = true;

    function playMusic(mute) {
        if (mute == 0) {
            music.play()
        }
    }
}