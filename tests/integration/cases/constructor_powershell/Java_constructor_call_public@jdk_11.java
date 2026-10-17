function Playlist { return 42 }

public Object p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
