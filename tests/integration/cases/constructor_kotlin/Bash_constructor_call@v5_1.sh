class Playlist { val value = 42 }

declare p="$(Playlist)"
check(p.value == 42)
