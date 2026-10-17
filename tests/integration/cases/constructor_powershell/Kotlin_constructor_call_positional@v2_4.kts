function Playlist { return 42 }

val p = Playlist()
if ($p -ne 42) { throw "Expected constructor result" }
