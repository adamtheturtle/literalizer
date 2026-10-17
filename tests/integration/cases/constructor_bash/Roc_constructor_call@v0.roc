Playlist() { printf '%s\n' 42; }

Val : [
    RList (List Val),
]
p = Playlist
[[ "$p" == 42 ]] || exit 1
