function Playlist { return 42 }

public static final Object p = new Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
