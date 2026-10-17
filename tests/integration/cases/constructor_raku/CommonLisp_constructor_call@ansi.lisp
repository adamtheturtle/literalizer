sub Playlist() { 42 }

(defparameter *p* (Playlist))
die "Expected constructor result" unless $p == 42;
