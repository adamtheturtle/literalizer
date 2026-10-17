Playlist() { printf '%s\n' 42; }

public static readonly object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
