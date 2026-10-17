type Playlist = object
    value: int

data Val
    = PList (Array Val)
p = Playlist
doAssert p.value == 0
