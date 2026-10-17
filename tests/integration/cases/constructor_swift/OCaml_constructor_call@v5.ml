struct Playlist { let value = 42 }

type val_t =
  | OList of val_t list
let p = Playlist()
precondition(p.value == 42)
