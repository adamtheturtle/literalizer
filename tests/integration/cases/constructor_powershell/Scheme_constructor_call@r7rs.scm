function Playlist { return 42 }

(define p (Playlist))
if ($p -ne 42) { throw "Expected constructor result" }
