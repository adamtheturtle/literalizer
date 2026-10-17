class Playlist { val value = 42 }

readonly object? p = new Playlist();
check(p.value == 42)
