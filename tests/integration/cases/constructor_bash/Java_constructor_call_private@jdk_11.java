Playlist() { printf '%s\n' 42; }

private Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
