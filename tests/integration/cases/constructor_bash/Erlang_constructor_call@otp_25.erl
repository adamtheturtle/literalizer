Playlist() { printf '%s\n' 42; }

P = 'Playlist'(),
[[ "$p" == 42 ]] || exit 1
