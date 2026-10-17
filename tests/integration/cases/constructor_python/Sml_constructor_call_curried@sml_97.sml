class Playlist:
    pass


datatype val_t =
    SList of val_t list
val p = Playlist
assert isinstance(p, Playlist)
