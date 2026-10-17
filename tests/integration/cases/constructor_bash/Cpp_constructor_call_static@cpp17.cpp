Playlist() { printf '%s\n' 42; }

static auto p = Playlist();
[[ "$p" == 42 ]] || exit 1
