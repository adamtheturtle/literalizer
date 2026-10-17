Playlist() { printf '%s\n' 42; }

let p = Playlist()
[[ "$p" == 42 ]] || exit 1
