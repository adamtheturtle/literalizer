class Playlist { val value = 42 }

datatype val_t =
    SList of val_t list
val p = Playlist()
check(p.value == 42)
