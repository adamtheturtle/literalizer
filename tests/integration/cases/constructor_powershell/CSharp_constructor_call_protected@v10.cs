function Playlist { return 42 }

protected object? p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
