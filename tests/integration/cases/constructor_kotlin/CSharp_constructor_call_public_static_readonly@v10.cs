class Playlist { val value = 42 }

public static readonly object? p = new Playlist();
check(p.value == 42)
