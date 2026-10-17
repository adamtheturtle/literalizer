struct Playlist { let value = 42 }

static const auto p = Playlist();
precondition(p.value == 42)
