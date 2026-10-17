Playlist() { printf '%s\n' 42; }

public object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
