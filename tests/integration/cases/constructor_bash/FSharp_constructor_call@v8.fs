Playlist() { printf '%s\n' 42; }

type Val =
    | FList of Val list
let p = Playlist()
[[ "$p" == 42 ]] || exit 1
