struct Playlist { let value = 42 }

(defparameter *p* (Playlist))
precondition(p.value == 42)
