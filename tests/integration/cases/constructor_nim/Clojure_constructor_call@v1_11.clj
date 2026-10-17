type Playlist = object
    value: int

(def p (Playlist))
doAssert p.value == 0
