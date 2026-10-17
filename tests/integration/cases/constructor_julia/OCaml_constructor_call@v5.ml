struct Playlist end

type val_t =
  | OList of val_t list
let p = Playlist()
@assert p isa Playlist
