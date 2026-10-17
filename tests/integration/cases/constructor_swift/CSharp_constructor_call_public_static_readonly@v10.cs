struct Playlist { let value = 42 }

public static readonly object? p = new Playlist();
precondition(p.value == 42)
