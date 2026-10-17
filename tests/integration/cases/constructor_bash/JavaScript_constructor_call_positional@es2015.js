Playlist() { printf '%s\n' 42; }

const p = new Playlist();
[[ "$p" == 42 ]] || exit 1
