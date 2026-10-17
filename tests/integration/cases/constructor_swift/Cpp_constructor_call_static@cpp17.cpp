struct Playlist { let value = 42 }

static auto p = Playlist();
precondition(p.value == 42)
