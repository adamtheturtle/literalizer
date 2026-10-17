Playlist() { printf '%s\n' 42; }

datatype val_t =
    SList of val_t list
val p = Playlist()
[[ "$p" == 42 ]] || exit 1
