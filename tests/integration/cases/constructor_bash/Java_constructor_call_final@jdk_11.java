Playlist() { printf '%s\n' 42; }

final Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
