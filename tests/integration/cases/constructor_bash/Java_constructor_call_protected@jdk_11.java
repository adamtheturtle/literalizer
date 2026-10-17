Playlist() { printf '%s\n' 42; }

protected Object p = new Playlist();
[[ "$p" == 42 ]] || exit 1
