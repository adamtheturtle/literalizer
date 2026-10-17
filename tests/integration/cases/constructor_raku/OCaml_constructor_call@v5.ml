sub Playlist() { 42 }

type val_t =
  | OList of val_t list
let p = Playlist()
die "Expected constructor result" unless $p == 42;
