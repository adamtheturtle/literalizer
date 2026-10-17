function Playlist { return 42 }

final p = Playlist();
if ($p -ne 42) { throw "Expected constructor result" }
