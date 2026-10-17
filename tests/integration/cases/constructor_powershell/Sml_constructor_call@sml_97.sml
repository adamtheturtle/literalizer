function Playlist { return 42 }

datatype val_t =
    SList of val_t list
val p = Playlist()
if ($p -ne 42) { throw "Expected constructor result" }
