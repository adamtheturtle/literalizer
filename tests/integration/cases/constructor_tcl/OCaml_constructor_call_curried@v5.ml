proc Playlist {} { return 42 }

type val_t =
  | OList of val_t list
let p = Playlist
if {$p != 42} { error "Expected constructor result" }
