Playlist() { printf '%s\n' 42; }

protected object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
