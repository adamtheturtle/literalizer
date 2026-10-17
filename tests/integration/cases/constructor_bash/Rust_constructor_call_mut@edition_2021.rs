Playlist() { printf '%s\n' 42; }

let mut p = Playlist::new();
[[ "$p" == 42 ]] || exit 1
