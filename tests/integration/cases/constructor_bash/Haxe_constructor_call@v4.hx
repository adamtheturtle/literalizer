Playlist() { printf '%s\n' 42; }

final p = new Playlist();
[[ "$p" == 42 ]] || exit 1
