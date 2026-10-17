Playlist() { printf '%s\n' 42; }

var p = new Playlist();
[[ "$p" == 42 ]] || exit 1
