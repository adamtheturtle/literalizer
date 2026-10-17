function Playlist { return 42 }

type val_t =
  | OList of val_t list
let p = Playlist()
if ($p -ne 42) { throw "Expected constructor result" }
