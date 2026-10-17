type Playlist = object
    value: int

type Val =
    | FList of Val list
let p = Playlist
doAssert p.value == 0
