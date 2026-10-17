Playlist() { printf '%s\n' 42; }

private protected object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
