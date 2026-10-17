type Playlist = object
    value: int

private object? p = new Playlist();
doAssert p.value == 0
