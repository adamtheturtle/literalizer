Playlist() { printf '%s\n' 42; }

: p Playlist ;
[[ "$p" == 42 ]] || exit 1
