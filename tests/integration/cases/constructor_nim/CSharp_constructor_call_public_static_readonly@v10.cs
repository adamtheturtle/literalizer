type Playlist = object
    value: int

public static readonly object? p = new Playlist();
doAssert p.value == 0
