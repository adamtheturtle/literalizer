Playlist() { printf '%s\n' 42; }

public Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
