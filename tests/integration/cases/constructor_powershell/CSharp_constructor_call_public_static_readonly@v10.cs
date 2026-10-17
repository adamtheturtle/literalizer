function Playlist { return 42 }

public static readonly object? p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
