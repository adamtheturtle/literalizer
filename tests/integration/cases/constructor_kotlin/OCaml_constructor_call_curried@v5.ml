class Playlist { val value = 42 }

type val_t =
  | OList of val_t list
let p = Playlist
check(p.value == 42)
