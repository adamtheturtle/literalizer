Playlist() { printf '%s\n' 42; }

p : A_Val := Playlist;
[[ "$p" == 42 ]] || exit 1
