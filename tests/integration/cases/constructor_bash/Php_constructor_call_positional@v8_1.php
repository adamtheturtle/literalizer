Playlist() { printf '%s\n' 42; }

$p = new Playlist();
[[ "$p" == 42 ]] || exit 1
