type Playlist = object
    value: int

type val_t =
  | OList of val_t list
let p = Playlist
doAssert p.value == 0
