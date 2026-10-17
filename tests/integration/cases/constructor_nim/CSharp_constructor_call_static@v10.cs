type Playlist = object
    value: int

static object? p = new Playlist();
doAssert p.value == 0
