proc Playlist {} { return 42 }

val p = Playlist()
if {$p != 42} { error "Expected constructor result" }
