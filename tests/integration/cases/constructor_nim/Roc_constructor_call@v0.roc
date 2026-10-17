type Playlist = object
    value: int

Val : [
    RList (List Val),
]
p = Playlist
doAssert p.value == 0
