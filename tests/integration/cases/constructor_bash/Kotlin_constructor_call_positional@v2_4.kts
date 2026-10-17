Playlist() { printf '%s\n' 42; }

val p = Playlist()
[[ "$p" == 42 ]] || exit 1
