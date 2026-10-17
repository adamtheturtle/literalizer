proc Playlist {} { return 42 }

(defparameter *p* (Playlist))
if {$p != 42} { error "Expected constructor result" }
