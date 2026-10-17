type Playlist = object
    value: int

let mut p = Playlist::new();
doAssert p.value == 0
