Playlist() { printf '%s\n' 42; }

var p = Playlist.new()
[[ "$p" == 42 ]] || exit 1
