Playlist() { printf '%s\n' 42; }

data Val = HList [Val]
p = Playlist
[[ "$p" == 42 ]] || exit 1
