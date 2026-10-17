proc Playlist {} { return 42 }

(def p (Playlist))
if {$p != 42} { error "Expected constructor result" }
