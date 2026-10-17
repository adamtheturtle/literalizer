type Playlist = object
    value: int

(defparameter *p* (Playlist))
doAssert p.value == 0
