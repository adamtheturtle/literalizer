function Playlist { return 42 }

$p = Playlist
if ($p -ne 42) { throw "Expected constructor result" }
