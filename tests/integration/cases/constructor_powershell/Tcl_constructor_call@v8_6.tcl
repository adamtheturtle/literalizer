function Playlist { return 42 }

set p [Playlist]
if ($p -ne 42) { throw "Expected constructor result" }
