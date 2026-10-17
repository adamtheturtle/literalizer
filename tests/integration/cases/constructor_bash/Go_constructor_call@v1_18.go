Playlist() { printf '%s\n' 42; }

p := NewPlaylist()
[[ "$p" == 42 ]] || exit 1
