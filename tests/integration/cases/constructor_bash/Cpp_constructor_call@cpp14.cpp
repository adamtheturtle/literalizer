Playlist() { printf '%s\n' 42; }

auto p = Playlist();
[[ "$p" == 42 ]] || exit 1
