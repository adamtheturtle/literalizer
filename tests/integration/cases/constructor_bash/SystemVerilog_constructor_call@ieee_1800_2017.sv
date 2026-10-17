Playlist() { printf '%s\n' 42; }

static _VVal p = Playlist();
[[ "$p" == 42 ]] || exit 1
