Playlist() { printf '%s\n' 42; }

type val_t =
  | OList of val_t list
let p = Playlist()
[[ "$p" == 42 ]] || exit 1
