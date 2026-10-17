function Playlist { return 42 }

id p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
