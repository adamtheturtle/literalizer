type Playlist = object
    value: int

data Val = HList [Val]
p = Playlist
doAssert p.value == 0
