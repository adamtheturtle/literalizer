Playlist() { printf '%s\n' 42; }

final p = Playlist();
[[ "$p" == 42 ]] || exit 1
