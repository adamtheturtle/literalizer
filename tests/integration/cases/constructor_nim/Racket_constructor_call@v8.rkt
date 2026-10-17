type Playlist = object
    value: int

(define p (Playlist))
doAssert p.value == 0
