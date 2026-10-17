Playlist() { printf '%s\n' 42; }

CVal p = Playlist();
[[ "$p" == 42 ]] || exit 1
