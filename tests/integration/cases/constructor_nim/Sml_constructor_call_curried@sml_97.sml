type Playlist = object
    value: int

datatype val_t =
    SList of val_t list
val p = Playlist
doAssert p.value == 0
