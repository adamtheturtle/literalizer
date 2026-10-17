Playlist() { printf '%s\n' 42; }

data Val
    = PList (Array Val)
p = Playlist
[[ "$p" == 42 ]] || exit 1
