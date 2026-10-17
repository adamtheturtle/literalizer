struct Playlist { let value = 42 }

static object? p = new Playlist();
precondition(p.value == 42)
