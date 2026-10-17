Playlist() { printf '%s\n' 42; }

p = Playlist.new()
[[ "$p" == 42 ]] || exit 1
