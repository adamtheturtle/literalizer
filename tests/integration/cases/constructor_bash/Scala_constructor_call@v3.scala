Playlist() { printf '%s\n' 42; }

val p = new Playlist()
[[ "$p" == 42 ]] || exit 1
