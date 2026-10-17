type Playlist = object
    value: int

readonly object? p = new Playlist();
doAssert p.value == 0
