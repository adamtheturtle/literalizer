Playlist() { printf '%s\n' 42; }

declare p="$(Playlist)"
[[ "$p" == 42 ]] || exit 1
