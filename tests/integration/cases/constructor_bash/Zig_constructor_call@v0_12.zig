Playlist() { printf '%s\n' 42; }

const p = Playlist();
[[ "$p" == 42 ]] || exit 1
