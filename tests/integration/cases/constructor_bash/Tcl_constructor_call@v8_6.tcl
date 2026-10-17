Playlist() { printf '%s\n' 42; }

set p [Playlist]
[[ "$p" == 42 ]] || exit 1
