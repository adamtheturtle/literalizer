Playlist() { printf '%s\n' 42; }

local p = Playlist()
[[ "$p" == 42 ]] || exit 1
