Playlist() { printf '%s\n' 42; }

(defparameter *p* (Playlist))
[[ "$p" == 42 ]] || exit 1
