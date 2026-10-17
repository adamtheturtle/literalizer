struct Playlist { let value = 42 }

static _VVal p = Playlist();
precondition(p.value == 42)
