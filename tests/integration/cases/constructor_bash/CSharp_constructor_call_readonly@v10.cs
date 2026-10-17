Playlist() { printf '%s\n' 42; }

readonly object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
