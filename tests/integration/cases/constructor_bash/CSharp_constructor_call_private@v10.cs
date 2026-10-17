Playlist() { printf '%s\n' 42; }

private object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
