Playlist() { printf '%s\n' 42; }

public static final Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
