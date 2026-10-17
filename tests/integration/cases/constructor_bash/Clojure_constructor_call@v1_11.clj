Playlist() { printf '%s\n' 42; }

(def p (Playlist))
[[ "$p" == 42 ]] || exit 1
