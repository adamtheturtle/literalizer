Playlist() { printf '%s\n' 42; }

id p = Playlist();
[[ "$p" == 42 ]] || exit 1
