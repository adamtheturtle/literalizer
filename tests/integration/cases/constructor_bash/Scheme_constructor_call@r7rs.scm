Playlist() { printf '%s\n' 42; }

(define p (Playlist))
[[ "$p" == 42 ]] || exit 1
