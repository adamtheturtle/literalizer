Playlist() { printf '%s\n' 42; }

let p = Playlist::new();
[[ "$p" == 42 ]] || exit 1
