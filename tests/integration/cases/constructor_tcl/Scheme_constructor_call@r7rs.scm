proc Playlist {} { return 42 }

(define p (Playlist))
if {$p != 42} { error "Expected constructor result" }
