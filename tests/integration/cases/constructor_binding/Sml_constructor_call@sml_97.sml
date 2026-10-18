fun Playlist _ = ()
datatype val_t =
    SList of val_t list
val created = Playlist()
val _ = created
