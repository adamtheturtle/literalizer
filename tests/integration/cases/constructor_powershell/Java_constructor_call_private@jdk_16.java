function Playlist { return 42 }

private Object p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
