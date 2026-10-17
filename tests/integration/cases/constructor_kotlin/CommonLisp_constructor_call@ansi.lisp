class Playlist { val value = 42 }

(defparameter *p* (Playlist))
check(p.value == 42)
