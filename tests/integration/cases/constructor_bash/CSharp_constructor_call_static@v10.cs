Playlist() { printf '%s\n' 42; }

static object? p = new Playlist();
[[ "$p" == 42 ]] || exit 1
