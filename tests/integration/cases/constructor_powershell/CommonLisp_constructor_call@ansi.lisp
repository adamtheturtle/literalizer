function Playlist { return 42 }

(defparameter *p* (Playlist))
if ($p -ne 42) { throw "Expected constructor result" }
