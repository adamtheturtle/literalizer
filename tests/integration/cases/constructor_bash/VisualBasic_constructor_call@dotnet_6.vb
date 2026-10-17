Playlist() { printf '%s\n' 42; }

Dim p = New Playlist()
[[ "$p" == 42 ]] || exit 1
