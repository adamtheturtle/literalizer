type Playlist = object
    value: int

declare p="$(Playlist)"
doAssert p.value == 0
