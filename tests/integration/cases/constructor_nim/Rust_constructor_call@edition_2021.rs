type Playlist = object
    value: int

let p = Playlist::new();
doAssert p.value == 0
