function Playlist { return 42 }

(def p (Playlist))
if ($p -ne 42) { throw "Expected constructor result" }
