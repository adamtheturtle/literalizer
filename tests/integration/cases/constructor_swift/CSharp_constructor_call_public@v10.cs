struct Playlist { let value = 42 }

public object? p = new Playlist();
precondition(p.value == 42)
