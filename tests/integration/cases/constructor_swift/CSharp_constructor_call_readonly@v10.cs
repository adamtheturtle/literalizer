struct Playlist { let value = 42 }

readonly object? p = new Playlist();
precondition(p.value == 42)
