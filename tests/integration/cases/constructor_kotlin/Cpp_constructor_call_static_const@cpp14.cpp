class Playlist { val value = 42 }

static const auto p = Playlist();
check(p.value == 42)
