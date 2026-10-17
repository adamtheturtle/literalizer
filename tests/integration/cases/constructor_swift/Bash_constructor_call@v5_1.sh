struct Playlist { let value = 42 }

declare p="$(Playlist)"
precondition(p.value == 42)
