Playlist() { printf '%s\n' 42; }

static Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
