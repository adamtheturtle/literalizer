Playlist() { printf '%s\n' 42; }

const auto p = Playlist();
[[ "$p" == 42 ]] || exit 1
