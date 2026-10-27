const music = document.getElementById("theme");

if (music) {
    music.volume = 0.05;
    music.loop = true;

    function playMusic(mute) {
        if (mute == 0) {
            music.play()
        }
    }
}