proc Playlist {} { return 42 }

datatype val_t =
    SList of val_t list
val p = Playlist()
if {$p != 42} { error "Expected constructor result" }
