function Playlist { return 42 }

CVal p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
