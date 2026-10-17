Playlist() { printf '%s\n' 42; }

static const auto p = Playlist();
[[ "$p" == 42 ]] || exit 1
