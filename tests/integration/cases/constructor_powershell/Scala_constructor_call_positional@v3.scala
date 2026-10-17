function Playlist { return 42 }

val p = new Playlist()
if ($p -ne 42) { throw "Expected constructor result" }
