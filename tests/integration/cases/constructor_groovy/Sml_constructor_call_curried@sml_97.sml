class Playlist {}

datatype val_t =
    SList of val_t list
val p = Playlist
assert p instanceof Playlist
