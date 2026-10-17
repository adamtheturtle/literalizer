Playlist() { printf '%s\n' 42; }

var p = Playlist()
[[ "$p" == 42 ]] || exit 1
