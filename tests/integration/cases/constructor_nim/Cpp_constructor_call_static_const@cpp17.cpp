type Playlist = object
    value: int

static const auto p = Playlist();
doAssert p.value == 0
